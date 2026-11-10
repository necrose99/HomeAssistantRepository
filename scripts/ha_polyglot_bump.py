#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HomeAssistant & Polyglot Overlay Ecosystem Bump Engine
Orchestrates node-ebuilder, cargo-ebuild, and pkgdev to automate multi-spec packages.
"""
import os
import re

OVERLAY_PATH = "/var/db/repos/homeassistant"
TARGET_KEYWORDS = 'KEYWORDS="amd64 arm arm64 x86 riscv64"'

# Compile a robust regular expression matching any keyword configuration array
keyword_regex = re.compile(r'KEYWORDS="[^"]*"')

print("🚀 Enforcing cluster architecture keywords across overlay tree...")

for root, _, files in os.walk(OVERLAY_PATH):
    for file in files:
        if file.endswith(".ebuild"):
            ebuild_path = os.path.join(root, file)
            
            with open(ebuild_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if keywords match our exact cluster array profile
            if TARGET_KEYWORDS not in content:
                print(f"📐 Balancing platform definitions inside: {file}")
                # Dynamically substitute whatever string was present
                content = keyword_regex.sub(TARGET_KEYWORDS, content)
                
                with open(ebuild_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Automatically trigger pkgdev manifest to sign off on the layout change
                subprocess.run(["pkgdev", "manifest"], cwd=root, check=True)

import os
import sys
import json
import subprocess
from pathlib import Path
from git import Repo

# --- TARGET ENVIROMENT MATRIX ---
OVERLAY_PATH = "/var/db/repos/homeassistant"
FUTURE_PYTHON_MATRIX = "python3_12 python3_13 python3_14 python3_15"
NODE_EBUILDER_CONFIG = "/etc/node-ebuilder/config.json5"


class PolyglotBumpEngine:
    def __init__(self, src_dir, overlay_path):
        self.src_dir = Path(src_dir)
        self.overlay_path = Path(overlay_path)
        self.pkg_name = self.src_dir.name.lower().replace("_", "-")
        
    def triage_and_generate(self):
        """Detects the underlying build framework and calls the matching generator."""
        has_cargo = (self.src_dir / "Cargo.toml").exists()
        has_pyproject = (self.src_dir / "pyproject.toml").exists()
        has_package_json = (self.src_dir / "package.json").exists()

        # Paradigm 1: Compiled Native Rust Crate (Standalone)
        if has_cargo and not has_pyproject:
            print(f"🦀 Rust Crate detected inside {self.src_dir}. Invoking cargo-ebuild...")
            self.execute_cargo_ebuild()

        # Paradigm 2: Polyglot Rust Extension for Python (Maturin Core)
        elif has_cargo and has_pyproject:
            print(f"🐍🦀 PyCargo/Maturin extension detected. Invoking pycargoebuild...")
            self.execute_pycargoebuild()

        # Paradigm 3: Node.js / TypeScript Ecosystem (Frontend/Zentyal modules)
        elif has_package_json:
            print(f"📦 Node.js framework detected. Invoking node-ebuilder via npmv1...")
            self.execute_node_ebuilder()

    def execute_cargo_ebuild(self):
        """Generates raw standalone Rust application ebuild configurations."""
        target_dir = self.overlay_path / "dev-util" / self.pkg_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Native cargo ebuild tracking command
        subprocess.run(["cargo", "ebuild", "--output", f"{target_dir}/{self.pkg_name}-9999.ebuild"], 
                       cwd=self.src_dir, check=True)
        self.finalize_package(target_dir)

    def execute_pycargoebuild(self):
        """Generates Maturin/PEP517-compliant extensions for modern Python targets."""
        target_dir = self.overlay_path / "dev-python" / self.pkg_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Invoke specialized pycargoebuild python-crate binding tool
        subprocess.run(["pycargoebuild", "--output", f"{target_dir}/{self.pkg_name}-9999.ebuild", "."], 
                       cwd=self.src_dir, check=True)
        self.finalize_package(target_dir)

    def execute_node_ebuilder(self):
        """Invokes geaaru's node-ebuilder to parse package.json dependencies."""
        target_dir = self.overlay_path / "www-apps" / self.pkg_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Executes node-ebuilder to map nested node_modules configurations
        cmd = ["node-ebuilder", "-c", NODE_EBUILDER_CONFIG, "-d", "--dir", str(self.src_dir)]
        subprocess.run(cmd, check=True)
        
        # Explicit override to drop inside your central local overlay tree
        generated_file = Path.home() / ".node-ebuilder" / "ebuilds" / f"{self.pkg_name}-9999.ebuild"
        if generated_file.exists():
            subprocess.run(["mv", str(generated_file), f"{target_dir}/{self.pkg_name}-9999.ebuild"], check=True)
        
        self.finalize_package(target_dir)

    def finalize_package(self, package_dir):
        """Injects your Python matrix array, generates manifests, and signs commits."""
        print(f"🛠️ Polishing generated metadata inside: {package_dir}")
        
        for file in os.listdir(package_dir):
            if file.endswith(".ebuild"):
                path = Path(package_dir) / file
                content = path.read_text()
                
                # Strip out old Python configurations if injected by pycargoebuild templates
                if "python3_11" in content or "PYTHON_COMPAT" not in content:
                    content = content.replace("python3_11", FUTURE_PYTHON_MATRIX)
                    path.write_text(content)
                
                # Enforce EAPI=8 if node-ebuilder outputs an old format
                if "EAPI=6" in content:
                    content = content.replace("EAPI=6", "EAPI=8")
                    path.write_text(content)

        # 1. pkgdev manifest signature pass
        subprocess.run(["pkgdev", "manifest"], cwd=package_dir, check=True)
        
        # 2. pkgdev automated format commit
        print("📝 Staging package into repository tree via pkgdev...")
        subprocess.run(["pkgdev", "commit", "-v", "-m", f"{self.pkg_name}: initial ingestion via polyglot automation loops"], 
                       cwd=package_dir, check=True)


if __name__ == "__main__":
    # Point this path straight to an active check-out loop of your infrastructure components
    test_src = "/tmp/home-assistant-frontend-clone"
    
    if os.path.exists(test_src):
        engine = PolyglotBumpEngine(test_src, OVERLAY_PATH)
        engine.triage_and_generate()
