# Maintainer: forkbong <panktist@gmail.com>
pkgname=dualtidy
pkgver=20150605
pkgrel=1
pkgdesc="Lightweight GTK tray battery monitor that supports more than one battery."
arch=('any')
url="https://github.com/forkbong/dualtidy"
license=('GPL3')
depends=(python3 gtk3 acpi)
makedepends=()
source=("https://raw.github.com/forkbong/dualtidy/master/${pkgname}.py")
sha256sums=('deb435c211eba9fec10c4f2ceae7e94f1e30c07a73071700d0c5112d3d5384fe')

package () {
   cd "$srcdir"
   install -Dm755 "${pkgname}.py" "${pkgdir}/usr/bin/dualtidy"
}
