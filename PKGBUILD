# Maintainer: forkbong <panktist@gmail.com>
pkgname=dualtidy
pkgver=20150523
pkgrel=1
pkgdesc="Lightweight GTK tray battery monitor that supports more than one battery."
arch=('any')
url="https://github.com/forkbong/dualtidy"
license=('GPL3')
depends=(python2 gtk2 acpi)
makedepends=()
source=("https://raw.github.com/forkbong/dualtidy/master/${pkgname}.py")
sha256sums=('5fa30891bd6123e75560a368e45098635974e2f878ee0a57dd8298a9377c7b1a')

package () {
   cd "$srcdir"
   install -Dm755 "${pkgname}.py" "${pkgdir}/usr/bin/dualtidy"
}
