# Copyright 1999-2026 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

# Strictly constrained to 6 due to npmv1.eclass _npmv1_set_metadata validation
EAPI=6

inherit git-r3 npmv1

DESCRIPTION="Ebuild file producer for nodejs modules"
HOMEPAGE="https://github.com"
EGIT_REPO_URI="https://github.com.git"
#eclass_url=https://github.com/geaaru/geaaru_overlay/blob/master/eclass%2Fnpmv1.eclass"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS=""

# Explicit structures processed via _npmv1_copy_dirs and NPM_BINS lookup loops
NPM_PKG_NAME="node-ebuilder"
NPM_PKG_DIRS="adapters etc"
NPM_BINS="
bin/node-ebuilder => node-ebuilder
"

src_unpack() {
	git-r3_src_unpack
}

# src_prepare, src_compile, and src_install are cleanly handled automatically 
# via inherited npmv1_src_* function maps.
