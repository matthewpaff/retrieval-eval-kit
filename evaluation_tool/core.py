"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value


def day(value):
    from datetime import date
    import re
    if not isinstance(value,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        raise ValueError("Use YYYY-MM-DD")
    return date.fromisoformat(value)


def text(value,maximum=10000):
    if not isinstance(value,str) or len(value)>maximum:
        raise ValueError("Expected bounded text")
    return value

def evaluate(data):
    fields(data,("k","queries"))
    k=integer(data["k"],1,100)
    seen,rows,recalls,ranks=set(),[],[],[]
    for query in sequence(data["queries"],500):
        fields(query,("id","relevant","ranked"))
        ident=label(query["id"])
        relevant=[label(item) for item in sequence(query["relevant"],100)]
        ranked=[label(item) for item in sequence(query["ranked"],100)]
        if ident in seen or len(set(relevant))!=len(relevant) or len(set(ranked))!=len(ranked):
            raise ValueError("Duplicate query or document ID")
        seen.add(ident)
        truth=set(relevant);top=ranked[:k]
        recall=len(truth&set(top))/len(truth) if truth else 0.0
        reciprocal=next((1/(index+1) for index,item in enumerate(top) if item in truth),0.0)
        recalls.append(recall);ranks.append(reciprocal)
        rows.append({"id":ident,"recall_at_k":round(recall,6),"reciprocal_rank_at_k":round(reciprocal,6)})
    count=len(rows)
    return {"queries":rows,"mean_recall_at_k":round(sum(recalls)/count,6) if count else 0.0,
        "mean_reciprocal_rank_at_k":round(sum(ranks)/count,6) if count else 0.0}
