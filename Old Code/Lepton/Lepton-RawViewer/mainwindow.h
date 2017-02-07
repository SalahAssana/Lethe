#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class QLabel;
class QPixmap;
class PixmapLabel;
class QSpinBox;
class QComboBox;

class MainWindow : public QMainWindow
{
    Q_OBJECT

    bool haveData;
    QLabel *value, *temp;
    PixmapLabel *pixmapLabel;

    void updatePixmapLabel(QImage rgbData);
    QVector<unsigned short> data;

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void clearData();

public slots:
    void newData(QString filePath);
    void mouseMoved(QPoint p);
};

#endif // MAINWINDOW_H
