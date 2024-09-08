import fitz
import re
from bs4 import BeautifulSoup
import pandas as pd
import spacy


def extract_annotations(filepath: str):
    dictt = { 
        'title': [],
        'sub_title':[],
        'sub_sub_title':[],
        'annotation':[]
    }
    title=""
    sub_title=""
    sub_sub_title=""
    doc = fitz.open(filepath)
    for i, page in enumerate(doc):
        page = page.get_text("html")
        soup = BeautifulSoup(page, "html.parser")
        spans = soup.find_all('span',style=True)
        for span in spans:
            if str(span['style']).find("font-size:16pt") != -1:
                title = span.text
                sub_title = ""
                sub_sub_title=""
                annotation=""
            elif str(span['style']).find("font-size:14pt") != -1:
                sub_title = span.text
                sub_sub_title=""
                annotation=""
            elif str(span['style']).find("font-size:12.5pt") != -1:
                sub_sub_title = span.text
                annotation=""
            elif title != "" and str(span['style']).find("font-size:10pt") == -1 and str(span['style']).find("font-size:9pt") == -1:
                annotation = span.text
                dictt['title'].append(title)
                dictt['sub_title'].append(sub_title)
                dictt['sub_sub_title'].append(sub_sub_title)
                dictt['annotation'].append(annotation)
    #dict to dataframe
    df = pd.DataFrame.from_dict(dictt).drop_duplicates().reset_index(drop=True)
    #merging annotations
    df = df.set_index(['title','sub_title','sub_sub_title']).stack().to_frame()
    df = df.groupby(['title', 'sub_title', 'sub_sub_title']).transform(lambda x: ','.join(x))
    df = df.drop_duplicates()
    
    return df

def learn_ontology(doc):
    subjects = []
    objects = []
    links = []
    ontologies = []

    #Extarcting subjects
    for token in doc:
        if token.dep_ in ['nsubj']:
            ontology = {'subject' : '-', 'link': [], 'object' : '-'}
            ontology['subject'] = token
            ontologies.append(ontology)

    #Extarcting links (verbs)
    for i in range(len(ontologies)):
        ontologies[i]['link'].append(ontologies[i]['subject'].head)
        if last_child(ontologies[i]['link'][-1]).dep_ in ['attr','prep','acomp']:
            ontologies[i]['link'].append(last_child(ontologies[i]['link'][-1]))
        elif last_child(ontologies[i]['link'][-1]).dep_ in ['case']:
            ontologies[i]['link'].append(ontologies[i]['link'][-1].head)

    #Extarcting objects
    for i in range(len(ontologies)):
        if last_child(ontologies[i]['link'][-1]):
            if last_child(ontologies[i]['link'][-1]).dep_ in ['pobj','dobj']:
                ontologies[i]['object'] = last_child(ontologies[i]['link'][-1])
            elif last_child(ontologies[i]['link'][-1].dep_ in['poss']):
                child = last_child(ontologies[i]['link'][-1])
                ontologies[i]['object'] = child
            else:
                child = last_child(ontologies[i]['link'][-1])
                ontologies[i]['object'] = last_child(child)

    return ontologies

        
def get_relations(spans_list):
    X_Relation_Y=[]
    for span in spacy.util.filter_spans(spans_list):
        X_Relation_Y.append(re.split('( include )',span.text))
        X_Relation_Y.append(re.split('( such as )',span.text))
        X_Relation_Y.append(re.split('( have )',span.text))
        X_Relation_Y.append(re.split('( is a )',span.text))
        X_Relation_Y.append(re.split('( part )',span.text))
        X_Relation_Y.append(re.split('( like )',span.text))
        X_Relation_Y.append(re.split('( kind of )',span.text))
        X_Relation_Y.append(re.split('( including )',span.text))
        X_Relation_Y.append(re.split('( instance )',span.text))
        X_Relation_Y.append(re.split('( and or other )',span.text))
        X_Relation_Y.append(re.split('( especially )',span.text))
        X_Relation_Y.append(re.split('( in )',span.text))

    df_X_Relation_Y = pd.DataFrame(X_Relation_Y,columns=['Y','Relation','X'])
    df_X_Relation_Y = df_X_Relation_Y[pd.notnull(df_X_Relation_Y.X)]
    df_X_Relation_Y.drop_duplicates()

    return df_X_Relation_Y