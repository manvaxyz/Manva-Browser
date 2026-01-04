#!/usr/bin/env python3
"""
MANVA AIOps orchestrator (prototype)

Responsibilities (prototype):
- Run local pipeline (build + tests) as gate
- Validate model registry contents
- Create a signed artifact stub
- Simulate k8s deployment (dry-run by default)
- Provide an auto-rollback hook (simulation)

This is a development stub to simulate AI-driven auto-deploy flows.
Replace model validation and signing with real cryptographic pipelines.
"""
import argparse
import subprocess
import requests
import sys
import time
import os
import yaml
from nacl import signing, encoding, exceptions


MODEL_REGISTRY = os.environ.get("MODEL_REGISTRY", "http://127.0.0.1:8083")
K8S_MANIFEST = os.path.join(os.path.dirname(__file__), "../../ops/deployment/k8s-sample.yaml")


def run_local_pipeline():
    print("[aiops] Running local CI pipeline...")
    try:
        subprocess.check_call(["/bin/bash", "./ops/ci/run-local-pipeline.sh"])
        print("[aiops] CI pipeline succeeded")
        return True
    except subprocess.CalledProcessError:
        print("[aiops] CI pipeline failed")
        return False


def validate_models():
    print(f"[aiops] Querying model registry at {MODEL_REGISTRY}")
    try:
        r = requests.get(f"{MODEL_REGISTRY}/models/list", timeout=5)
        r.raise_for_status()
        data = r.json()
        models = data.get("models", [])
        print(f"[aiops] Found {len(models)} model(s)")
        # Prototype rule: require at least one model named intent-v1
        for m in models:
            if m.get("name") == "intent-v1":
                print("[aiops] Required model intent-v1 present")
                return True
        print("[aiops] Required model not found")
        return False
    except Exception as e:
        print("[aiops] Model validation error:", e)
        return False


def sign_artifact(artifact_path: str):
    # Ed25519 signing: create keypair if needed and sign artifact
    keydir = os.path.expanduser("~/.manva/keys")
    os.makedirs(keydir, exist_ok=True)
    sk_path = os.path.join(keydir, "ed25519_sk")
    pk_path = os.path.join(keydir, "ed25519_pk")

    if not os.path.exists(sk_path) or not os.path.exists(pk_path):
        print("[aiops] Generating new Ed25519 keypair for signing")
        sk = signing.SigningKey.generate()
        pk = sk.verify_key
        with open(sk_path, "wb") as f:
            f.write(sk.encode())
        with open(pk_path, "wb") as f:
            f.write(pk.encode())
    else:
        with open(sk_path, "rb") as f:
            sk = signing.SigningKey(f.read())

    # read artifact and sign
    with open(artifact_path, "rb") as f:
        data = f.read()

    signed = sk.sign(data)
    sig_path = artifact_path + ".sig"
    with open(sig_path, "wb") as f:
        f.write(signed.signature)

    # write public key for verification reference
    with open(pk_path, "rb") as f:
        pkb = f.read()

    print(f"[aiops] Signed artifact -> {sig_path}")
    print(f"[aiops] Public key at {pk_path}")
    return sig_path


def verify_signature(artifact_path: str, sig_path: str, pk_path: str) -> bool:
    try:
        with open(pk_path, "rb") as f:
            pk = signing.VerifyKey(f.read())
        with open(artifact_path, "rb") as f:
            data = f.read()
        with open(sig_path, "rb") as f:
            sig = f.read()
        # verify expects signature+message; build signed blob for verification
        signed_blob = sig + data
        pk.verify(signed_blob)
        return True
    except (exceptions.BadSignatureError, Exception) as e:
        print("[aiops] Signature verification failed:", e)
        return False


def deploy(dry_run=True):
    print(f"[aiops] Deploying manifests (dry_run={dry_run}) -> {K8S_MANIFEST}")
    # Use kubectl client-side dry-run by default
    cmd = ["kubectl", "apply", "-f", K8S_MANIFEST]
    if dry_run:
        cmd.insert(2, "--dry-run=client")
    try:
        subprocess.check_call(cmd)
        print("[aiops] kubectl apply succeeded")
        return True
    except FileNotFoundError:
        print("[aiops] kubectl not found; skipping real apply (simulating)")
        return True
    except subprocess.CalledProcessError as e:
        print("[aiops] kubectl apply failed:", e)
        return False


def auto_rollback(reason: str):
    print(f"[aiops] Auto-rollback triggered (reason={reason}) — simulating rollback to previous signed release")
    # Prototype rollback: log and return success
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--no-dry-run", dest="dry", action="store_false", help="Perform real kubectl apply if available")
    args = parser.parse_args()

    while True:
        ok = run_local_pipeline()
        if not ok:
            auto_rollback("ci-failed")
            if args.once:
                sys.exit(1)
            time.sleep(30)
            continue

        vm_ok = validate_models()
        if not vm_ok:
            auto_rollback("model-validation-failed")
            if args.once:
                sys.exit(1)
            time.sleep(30)
            continue

        # Build artifact stub
        artifact = "manva-artifact-0.1.0.tar.gz"
        open(artifact, "w").write("artifact-stub")
        sig = sign_artifact(artifact)

        deployed = deploy(dry_run=args.dry)
        if not deployed:
            auto_rollback("deploy-failed")
            if args.once:
                sys.exit(1)
        else:
            print("[aiops] Deployment simulated successfully — scheduling post-deploy checks")

        if args.once:
            break

        # Sleep between checks — in production, this would be event driven
        time.sleep(60)


if __name__ == "__main__":
    main()
