#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>
#include <QLabel>
#include <QPushButton>
#include <QGridLayout>
#include <QImage>
#include <QPixmap>
#include <QFile>
#include <QTextStream>
#include <QPainter>
#include <QtCore>
#include <QButtonGroup>
#include <QFont>
#include <QDir>
#include <QDate>

#include "LEPTON_SDK.h"
#include "LEPTON_SYS.h"

class QLabel;
class LeptonThread;
class QGridLayout;
class QLineEdit;
class QPushButton;
class QButtonGroup;


class MainWindow : public QMainWindow {
    Q_OBJECT

    enum { ImageWidth = 320, ImageHeight = 240 };

    int snapshotCount;
    LEP_CAMERA_PORT_DESC_T portDesc;

    QLabel *imageLabel, *info;
    LeptonThread *thread;
    QGridLayout *layout;

    unsigned short rawMin, rawMax;
    QVector<unsigned short> rawData;
    QImage rgbImage;

public:
    explicit MainWindow(QWidget *parent = 0);

public slots:
    void saveSnapshot();
    void updateImage(unsigned short *, int, int);
};

#endif // MAINWINDOW_H
