package main

import (
    "encoding/json"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(map[string]interface{}{"ok": true, "status": "ready"})
    })

    http.HandleFunc("/models/list", func(w http.ResponseWriter, r *http.Request) {
        // Stub: return a static list of signed models
        json.NewEncoder(w).Encode(map[string]interface{}{"ok": true, "models": []map[string]string{{"name": "intent-v1", "version": "0.1.0", "signature": "dev-sig"}}})
    })

    log.Println("model-registry listening on :8083")
    log.Fatal(http.ListenAndServe(":8083", nil))
}
