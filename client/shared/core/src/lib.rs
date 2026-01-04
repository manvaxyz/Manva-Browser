use regex::Regex;
use serde::Serialize;
use std::collections::HashMap;

#[derive(Debug, Serialize, Clone)]
pub struct IntentResult {
    pub intent: String,
    pub confidence: f32,
    pub entities: HashMap<String, String>,
}

/// Parse a short user command into intent and entities.
/// This is a deterministic, lightweight parser intended as a drop-in
/// on-device fallback while larger models run separately.
pub fn parse_intent(input: &str) -> IntentResult {
    let t = input.trim();
    let mut entities = HashMap::new();
    // simple patterns
    let re_search = Regex::new(r"(?i)^search\s+(.+)").unwrap();
    let re_open = Regex::new(r"(?i)^open\s+(.+)").unwrap();
    let re_summarize = Regex::new(r"(?i)summary|summarize").unwrap();

    if let Some(c) = re_search.captures(t) {
        entities.insert("query".into(), c.get(1).unwrap().as_str().to_string());
        return IntentResult { intent: "search".into(), confidence: 0.95, entities };
    }

    if let Some(c) = re_open.captures(t) {
        entities.insert("target".into(), c.get(1).unwrap().as_str().to_string());
        return IntentResult { intent: "open".into(), confidence: 0.9, entities };
    }

    if re_summarize.is_match(t) {
        return IntentResult { intent: "summarize".into(), confidence: 0.85, entities };
    }

    // fallback heuristic: if input contains a URL-looking string, open
    let re_url = Regex::new(r"https?://[\w\.-]+").unwrap();
    if let Some(m) = re_url.find(t) {
        entities.insert("url".into(), m.as_str().to_string());
        return IntentResult { intent: "open".into(), confidence: 0.8, entities };
    }

    // unknown
    IntentResult { intent: "unknown".into(), confidence: 0.4, entities }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search() {
        let r = parse_intent("Search Rust async tutorials");
        assert_eq!(r.intent, "search");
        assert!(r.confidence > 0.9);
        assert_eq!(r.entities.get("query").unwrap(), "Rust async tutorials");
    }

    #[test]
    fn test_open_url() {
        let r = parse_intent("open https://example.com/page");
        assert_eq!(r.intent, "open");
        assert!(r.entities.contains_key("target") || r.entities.contains_key("url"));
    }

    #[test]
    fn test_summarize() {
        let r = parse_intent("Please summarize this article");
        assert_eq!(r.intent, "summarize");
    }
}
