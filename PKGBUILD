# Maintainer: forkbong <panktist@gmail.com>
pkgname=dualtidy
pkgver=20150523
pkgrel=1
pkgdesc="Lightweight GTK tray battery monitor that supports more than one battery."
arch=('any')
url="https://github.com/forkbong/dualtidy"
license=('GPL3')
depends=(python3 gtk3 acpi)
makedepends=()
source=("https://raw.github.com/forkbong/dualtidy/master/${pkgname}.py")
sha256sums=('a1a9ca43488f06dce0921f85d5dc5daea243927648a9109b90eb6b958117a6bf')

package () {
   cd "$srcdir"
   install -Dm755 "${pkgname}.py" "${pkgdir}/usr/bin/dualtidy"
}
