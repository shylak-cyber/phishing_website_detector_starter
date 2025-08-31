
import re
import math
from urllib.parse import urlparse
import tldextract
import numpy as np

SUSPICIOUS_TLDS = {
    "zip","xyz","top","gq","work","tk","ml","cf","ru","click","country","stream","download","men",
    "party","loan","kim","mom","date","racing","science","study","buzz"
}

SHORTENERS = {"bit.ly","goo.gl","t.co","tinyurl.com","ow.ly","is.gd","buff.ly","adf.ly","bit.do","mcaf.ee"}

IP_REGEX = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    data = s.encode('utf-8', 'ignore')
    length = len(data)
    if length == 0:
        return 0.0
    counts = {}
    for b in data:
        counts[b] = counts.get(b, 0) + 1
    ent = 0.0
    for c in counts.values():
        p = c / length
        ent -= p * math.log2(p)
    return ent

def has_ip(host):
    return bool(IP_REGEX.match(host))

def extract(url: str) -> np.ndarray:
    try:
        if not url.startswith(("http://","https://")):
            url = "http://" + url
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
        full = parsed.geturl()
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        subdomain = ext.subdomain or ""
        tld = ext.suffix.split(".")[-1] if ext.suffix else ""

        feats = {}
        feats["url_len"] = len(full)
        feats["host_len"] = len(host)
        feats["path_len"] = len(path)
        feats["num_dots"] = full.count(".")
        feats["num_hyphens"] = full.count("-")
        feats["num_at"] = full.count("@")
        feats["num_qm"] = full.count("?")
        feats["num_pct"] = full.count("%")
        feats["num_eq"] = full.count("=")
        feats["num_slash"] = full.count("/")
        feats["num_digits"] = sum(c.isdigit() for c in full)
        feats["digit_ratio"] = feats["num_digits"] / max(1, feats["url_len"])
        feats["entropy"] = shannon_entropy(full)
        feats["is_https"] = 1 if parsed.scheme == "https" else 0
        feats["has_ip_host"] = 1 if has_ip(host) else 0
        feats["num_subdomains"] = subdomain.count(".") + (1 if subdomain else 0)
        feats["suspicious_tld"] = 1 if tld in SUSPICIOUS_TLDS else 0
        feats["shortener"] = 1 if domain in SHORTENERS else 0
        feats["starts_with_https"] = 1 if full.lower().startswith("https") else 0
        feats["has_double_slash_in_path"] = 1 if "//" in path.strip("/") else 0
        feats["num_params"] = query.count("&") + (1 if query else 0)
        feats["path_depth"] = len([p for p in path.split("/") if p])
        feats["num_period_in_path"] = path.count(".")
        feats["num_reserved"] = sum(full.count(c) for c in [";","_","~","!","*","(",")",","])

        ordered = ["url_len","host_len","path_len","num_dots","num_hyphens","num_at","num_qm","num_pct",
                   "num_eq","num_slash","num_digits","digit_ratio","entropy","is_https","has_ip_host",
                   "num_subdomains","suspicious_tld","shortener","starts_with_https","has_double_slash_in_path",
                   "num_params","path_depth","num_period_in_path","num_reserved"]

        return np.array([feats[k] for k in ordered], dtype=float), feats, ordered
    except Exception:
        ordered = ["url_len","host_len","path_len","num_dots","num_hyphens","num_at","num_qm","num_pct",
                   "num_eq","num_slash","num_digits","digit_ratio","entropy","is_https","has_ip_host",
                   "num_subdomains","suspicious_tld","shortener","starts_with_https","has_double_slash_in_path",
                   "num_params","path_depth","num_period_in_path","num_reserved"]
        return np.zeros(len(ordered)), {k:0 for k in ordered}, ordered
