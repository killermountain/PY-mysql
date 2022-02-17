from rake_nltk import Rake
from connDB import MySQLDB

nltk.download('stopwords')

def GetKeywords(text, unique=True):
    r = Rake()
    # Extraction given the text.
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    # keywords = r.get_ranked_phrases_with_scores()
    if unique:
        return list(dict.fromkeys(keywords))
    else:
        return keywords

def checkAndUpdate(docsCount, lastID, docs=None):
    conn_db = MySQLDB()
    newCount, newlastID = conn_db.getDocInfo()

    if newCount == docsCount and newlastID == lastID:
        """return [docs, docsCount, lastID]"""
    else:                       # Data Update
        docs = conn_db.getAllDocs()
        docsCount, lastID = newCount, newlastID
        print("Doc files updated")
    conn_db.disconnectDB()    
    return [docs, docsCount, lastID]

def searchDocs(query, docs, docsCount, lastID, top_x=5):

        results={}
        query_keys = GetKeywords(query)
        updated = checkAndUpdate(docsCount, lastID)
        if updated[0]: # Updated
            results["docs"] = updated[0]
        else: # keep the old ones
            results["docs"] = docs
        results["docCount"] = updated[1]
        results["docLastID"] = updated[2]
        score = {}
        
        for doc_row in results["docs"]:
            doc_name = doc_row[1]
            for key in query_keys:
                score[doc_name] = score.get(doc_name, 0) + doc_row[3].count(key)

        results["matches"] = dict(sorted(score.items(), key=lambda item: item[1], reverse=True)[:top_x])
        return results

def searchElements():
    """searching elements"""

if __name__ == "__main__":
    inp_query = "risk assessment"
    results = searchDocs(inp_query,None, None,None, 3)
    print(results["docCount"])
    print(results["docLastID"])
    print(results["matches"])
    


