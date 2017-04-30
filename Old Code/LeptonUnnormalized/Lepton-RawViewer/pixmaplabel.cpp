#include "pixmaplabel.h"

#include <QMouseEvent>
#include <QDropEvent>
#include <QMimeData>
#include <QDebug>

PixmapLabel::PixmapLabel(QWidget *parent) :
    QLabel(parent),currentPoint(-1, -1)
{
    setAcceptDrops(true);
}

void PixmapLabel::mouseMoveEvent(QMouseEvent *e) {
    int x = e->x(), y = e->y();
    if ((x%8==0) || (y%8==0)) return;
    QPoint newPoint(x/8, y/8);
    if (newPoint != currentPoint)
        emit mouseMoved(newPoint);
}

void PixmapLabel::dragEnterEvent(QDragEnterEvent *e)
{
    if (e->mimeData()->hasUrls()) {
        QUrl url = e->mimeData()->urls().first();
        if (url.isLocalFile()) e->acceptProposedAction();
    }
}

void PixmapLabel::dropEvent(QDropEvent *e) {
    QUrl url = e->mimeData()->urls().first();
    emit fileDropped(url.toLocalFile());
}
