#ifndef PIXMAPLABEL_H
#define PIXMAPLABEL_H

#include <QLabel>

class PixmapLabel : public QLabel
{
    Q_OBJECT
    QPoint currentPoint;

public:
    explicit PixmapLabel(QWidget *parent = 0);

    virtual void dragEnterEvent(QDragEnterEvent *e);
    virtual void mouseMoveEvent(QMouseEvent *e);
    virtual void dropEvent(QDropEvent *e);

signals:
    void mouseMoved(QPoint p);
    void fileDropped(QString filePath);

public slots:

};

#endif // PIXMAPLABEL_H
