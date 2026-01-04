Android app skeleton for MANVA.

This folder contains a minimal skeleton and notes for the Android application. The real app should use Kotlin + Jetpack Compose and call into the shared Rust core via JNI for renderer and AI bindings.

Next steps:
- Add `app` Gradle module and configure Kotlin, Compose and NDK for Rust library bindings.
- Implement JNI layer connecting to shared Rust core.
