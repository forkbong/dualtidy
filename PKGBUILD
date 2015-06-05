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
sha256sums=('ececd7e6c37ad1de1a018644de98facb62e63bab979ddb8aac67149d0538bcd3')

package () {
   cd "$srcdir"
   install -Dm755 "${pkgname}.py" "${pkgdir}/usr/bin/dualtidy"
}
