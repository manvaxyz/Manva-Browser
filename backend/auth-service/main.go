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

    http.HandleFunc("/auth/otp", func(w http.ResponseWriter, r *http.Request) {
        // Stub: accept any OTP for development. Replace with secure OTP delivery and verification.
        json.NewEncoder(w).Encode(map[string]interface{}{"ok": true, "token": "dev-ephemeral-token"})
    })

    log.Println("auth-service listening on :8081")
    log.Fatal(http.ListenAndServe(":8081", nil))
}
