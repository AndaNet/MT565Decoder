
import re
import os
import pandas as pd
import glob
import os
import warnings

warnings.filterwarnings('ignore')


def validateFile(filepath, filename, text):
    MESSAGE_REGEX = re.compile(
        r"^"
        r"({1:(?P<basic_header>[^}]+)})?"
        r"({2:(?P<application_header>(I|O)[^}]+)})?"
        r"({3:"
            r"(?P<user_header>"
                r"({113:[A-Z]{4}})?"
                r"({108:[A-Z 0-9]{0,16}})?"
                r"({111:[0-9]{3}})?"
                r"({121:[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-4[a-zA-Z0-9]{3}-[89ab][a-zA-Z0-9]{3}-[a-zA-Z0-9]{12}})?"  # NOQA: E501
            r")"
        r"})?"
        r"({4:\s*(?P<text>.+?)\s*-})?"
        r"({5:(?P<trailer>.+)})?"
        r"$",
        re.DOTALL,)
      
    m = MESSAGE_REGEX.match(text)
               
    return m.group('text')    
    
    
def validate(filename,text):
    
    TEXT_REGEX = re.compile(
        r"^"
        r"(:16R:(?P<genl_start_block>(GENL))[^:]*)?"
        r"(:20C::COAF//(?P<Official_Corporate_Action_Event>[^:]*))?"
        r"(:20C::CORP//(?P<Corporate_Action_Reference>[^:]*))?"
        r"(:20C::SEME//(?P<Sender_Message_Reference>[^:]*))?"
        r"(:23G:(?P<Function_of_Message>(CANC|NEWM)[^:]*))?" 
        r"(:23G:(?P<Sub_Function_of_Message>(CODU|COPY|DUPL))[^:]*)?" 
        r"(:22F::CAEV//(?P<Corporate_Action_Event_Indicator>[^:]*))?"
        r"(:98[AC]::PREP//(?P<Preparation_Date_Time>\d{8,14})[^:]*)?"
        r"(:16S:(?P<genl_end_block>(GENL))[^:]*)?" 
        r"(:16R:(?P<USECU_start_block>(USECU))[^:]*)?"
        r"(:35B:(?P<Identification_of_the_Financial_Instrument>(ISIN)\s[a-zA-Z0-9]{12})[^:]*)?"
        r"(:35B:(?P<Descr_Identification_of_the_Financial_Instrument>[^:]*))?"
        r"(:16R:(?P<ACCTINFO_start_block>(ACCTINFO))[^:]*)?" 
        r"(:97A::SAFE//(?P<Safekeeping_Account>[^:]*))?"
        r"(:16S:(?P<ACCTINFO_end_block>(ACCTINFO))[^:]*)?"
        r"(:16S:(?P<USECU_end_block>(USECU))[^:]*)?"
        r"(:16R:(?P<CAINST_start_block>(CAINST))[^:]*)?"
        r"(:13A::CAON//(?P<Corporate_Action_Option_Number>[^:]*))?"
        r"(:22[FH]::CAOP//(?P<Corporate_Action_Option_Code>[^:]*))?" 
        r"(:36B::"
        r"(?P<Type_Code_Financial_Instrument_class>(COND|QINS))//"
        r"(?P<Quantity_Type_Code_of_Financial_Instrument>(AMOR|FAMT|UNIT))/"
        r"(?P<Quantity_Financial_Instrument>[^:]*)"
        r")*?" 
        r"(:36C::"
        r"(?P<Code_Financial_Instrument_class>(COND|QINS))//"
        r"(?P<Quantity_Code_of_Financial_Instrument>(QALL))"          
        r")*?"
        r"(:70E::"
        r"(?P<Narrative_class>(COMP|DLVR|FXIN|INST))/"
        r"(?P<Narrative>[^:]*)"          
        r")*?" 
        r"(:16S:(?P<CAINST_end_block>(CAINST))[^:]*)?"                         
        r"$",     
        re.DOTALL,
    )  
  
    
    m = TEXT_REGEX.match(text)
    if not bool(m):
        "File "+filename+" schema not matching"        
    
    dict = {}
    
    dict = m.groupdict()
    dict["FileName"] = filename
    
    df = pd.DataFrame()
    output= df.append(dict, ignore_index=True)
    output = output.replace('\n','', regex=True)
    output.to_csv(filename,index=False)
    
    
    
  

    
    
if __name__ == "__main__":
    


    dir_path = r'path'
    for filename in os.listdir(dir_path):      
        if os.path.isfile(os.path.join(dir_path, filename)):
            with open(str(os.path.join(dir_path, filename)),'r') as f:
               content = f.read()
               text =validateFile(str(os.path.join(dir_path, filename)), filename,content)   
               validate(filename,str(text))
    