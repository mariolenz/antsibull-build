# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project, 2024

"""
Code to lint build data.
"""

from __future__ import annotations

import os

from antsibull_changelog.lint import lint_changelog_yaml as _lint_changelog_yaml
from antsibull_core import app_context
from antsibull_core.collection_meta import lint_collection_meta as _lint_collection_meta
from antsibull_core.dependency_files import parse_pieces_file


def lint_build_data() -> int:
    """Lint build data."""
    app_ctx = app_context.app_ctx.get()

    major_release: int = app_ctx.extra["ansible_major_version"]
    data_dir: str = app_ctx.extra["data_dir"]
    pieces_file: str = app_ctx.extra["pieces_file"]

    all_collections = parse_pieces_file(os.path.join(data_dir, pieces_file))

    # Lint collection-meta.yaml
    errors = _lint_collection_meta(
        collection_meta_path=os.path.join(data_dir, "collection-meta.yaml"),
        major_release=major_release,
        all_collections=all_collections,
    )

    # Lint changelog.yaml
    changelog_path = os.path.join(data_dir, "changelog.yaml")
    for path, _, __, message in _lint_changelog_yaml(
        changelog_path, no_semantic_versioning=True, strict=True
    ):
        errors.append(f"{path}: {message}")

    # Show results
    for message in sorted(errors):
        print(message)

    return 3 if errors else 0
