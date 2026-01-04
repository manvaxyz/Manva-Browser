use manva_core::parse_intent;
use serde_json::to_string_pretty;

fn main() {
    println!("MANVA Desktop Shell prototype — starting...");
    let sample = "Search latest performance tips for Rust";
    let result = parse_intent(sample);
    println!("Parsed intent (sample):\n{}", to_string_pretty(&result).unwrap());
    println!("This is a minimal prototype. Replace with real renderer and UI.");
}
