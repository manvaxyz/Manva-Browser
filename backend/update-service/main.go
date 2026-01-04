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

    http.HandleFunc("/update/check", func(w http.ResponseWriter, r *http.Request) {
        // Stub: always report latest version available.
        json.NewEncoder(w).Encode(map[string]interface{}{"ok": true, "version": "0.1.0", "url": "https://updates.example/manva/0.1.0/"})
    })

    log.Println("update-service listening on :8082")
    log.Fatal(http.ListenAndServe(":8082", nil))
}
