

# Project Lethe: Privacy-Preserving Indoor Localization System

Named after [the river Lethe](https://en.wikipedia.org/wiki/Lethe) from Greek mythology, project Lethe is a privacy-preserving indoor localization system designed to allow for room-level localization of individuals in a home or building. The system preserves user anonymity by using a novel detection algorithm that limits both the memory available onboard the camera and the data rate of camera communication to prevent a full image from being extracted. Briefly, the algorithm detects the direction of movement by breaking the camera's FOV into three quadrants and tracking the order in which the person enters and exits each quadrant.

# System Design

Lethe consists of both a custom-built hardware system and a novel data processing pipeline.

## Hardware Components

### FLIR Thermal Sensor

The system utilizes a [FLIR Lepton Thermal Imaging Module](https://www.sparkfun.com/products/16465) as the main component of its detection module. The thermal imager captures infrared radiation input in its nominal response wavelength band (from 8 to 14 microns) and has a thermal sensitivity of 50 milli-Kelvins. The imager has an effective frame rate of 8.6 Hz and a resolution of 60 (w) × 80 (h) active pixels (each 17 μm in size and covering a 0.6375-degree angle).

### Breakout Board

The thermal imager is embedded in a breakout board which provides the socket for the Lepton, on-board power supplies, 25Mhz reference clock (can be by-passed), power-efficient 1.2v core voltage (can be by-passed), dual low noise LDO for 2.8V voltage (can be by-passed), 100 mil header for use in a breadboard or wiring to any host system. A few things to consider about this kit: the breakout board will accept a 3-5.5V input and regulate it to what the Lepton® wants, to read an image from the lepton module all you need is an SPI port, and to configure the camera settings you also need an I2C port, although this is not required.

### Raspberry Pi 1

Frames obtained by the thermal imager are sent over an SPI port to the Pi, where each pixel is processed independently and then permanently deleted. The stream of pixel values is processed by a novel algorithm that determines the direction of the crossing.

## Software Components

### Customized Driver

The FLIR Thermal Module is operated using a custom written driver which uses a limited memory buffer to transfer one pixel at a time.

### Presence Detection

We detect the presence of a person in the field of view based on their temperature. Indoor environments are typically air-conditioned to a 20°C to 22°C range and most objects in the environment conform to this temperature. Human skin temperature ranges between 32°C and 34°C. Additionally, hair and clothing tend to absorb the skin’s heat and retain a temperature lower than skin temperature, but higher than the surrounding environment (e.g., 25°C to 30°C). Hence, a person can be detected in the view of a thermal camera by identifying pixels that are warmer than the background temperature. . In Lethe, we determine the background temperature $r_{back}$ as the average temperature of the last frame absent human presence. This value is updated with each new human-less frame to adjust the background temperature to changes in the environment temperature. We detect a human in a pixel whenever that pixel has a value $r_{thresh}$ degrees higher than the background reference $r_{back}$ . If at any point in the streaming evaluation of a frame a pixel passes this threshold, the frame is declared as having a presence. If this is the beginning of an event, $t_s$ is updated. Once a person is detected, we consider all frames 0.366 seconds after the last frame with a presence ( $t_last$) to be part of the event. This aims to cover any gap caused by lost frames in an event, without merging two events in succession. This lag time value is conservatively based on the average walking speed of a person (1.39 m/s) and the average shoulder span of an adult male (0.508 m)

### Direction Detection

Once presence detection has ended an event with the creation of the ( $t_s$, $t_e$) tuple, direction detection either assigns a direction d to that event or removes that event as a non-crossing interaction. Direction detection collects the information needed to make this determination in parallel to presence detection. Each streaming pixel evaluated by presence detection is also used by direction. Direction detection uses the same $r_{back}$ and $r_{thresh}$ as presence to determine if someone is present in a pixel. However, direction detection goes beyond presence to use this information to determine a person’s location in the frame and how that location changes over time. When a person crosses through the field of view they first appear on one side of the frame and then progress in intervals to the other side before leaving the field of view. A canonical example of this behavior can be seen in the figure above. Lethe captures the progress of the person over time through the field of view by leftmost sector and rightmost sector location of the person in frame $i$. If the pixels of a frame are processed from left to right, this means Lethe sets $loc$ to the column of the first pixel with a human presence and loci to the column of the last pixel with a human presence. In this way, Lethe identifies the region a person is located in for each frame.

# Privacy Preserving Algorithm

The Lethe thermal camera requires only 21 values in memory for it's operation. For the detection algorithms, 4 values are required for presence detection ( $t_s$, $t_e$, $r_{back}$, $t_last$), 12 values for direction ( $loc_{l1}^i$, $loc_{r1}^i$, $loc_{l1}^{i-1}$, $loc_{r1}^{i-1}$, $d_{ind1}$, $d_{sum1}$, $loc_{l2}^i$, $loc_{r2}^i$, $loc_{l2}^{i-1}$, $loc_{r2}^{i-1}$, $d_{ind2}$, $d_{sum2}$), and a single value for pixel height detection ( $h_{pixel}$). Additionally, the thermal camera requires space to store the current pixel temperature the current location of the pixel (row and column), and the current time of the device. Reference information, such as the height and width of the image, the lag time allowed in frames, and the $r_{thresh}$ value can be kept statically. Many of the dynamic values, depending on the size of the image, can be represented using a single byte. Only the timestamps require a larger storage space at 4 bytes a piece. Hence the memory requirement for the Lethe thermal camera is only $M=33$ bytes. In the 60x80 pixel thermal camera used in this work, that means only 33 pixels (0.69\%) of the image can ever be stored on the device.

# Cross Detection

Once presence detection has ended an event with the creation of the ( $t_s$,$t_e$) tuple, direction detection either assigns a direction $d$ to that event or removes that event as a non-crossing interaction. Direction detection collects the information needed to make this determination in parallel to presence detection. Each streaming pixel evaluated by presence detection is also used by direction. Direction detection uses the same $r_{back}$ and $r_{thresh}$ as presence to determine if someone is present in a pixel. However, direction detection goes beyond presence to use this information to determine a person's location in the frame and how that location changes over time. When a person crosses through the field of view they first appear on one side of the frame and then progress in intervals to the other side before leaving the field of view. A canonical example of this behavior can be seen in the figure above. Lethe captures the progress of the person over time through the field of view by leftmost, $loc_l^i$, and rightmost, $loc_r^i$, the location of the person in frame $i$. If the pixels of a frame are processed from left to right, this means Lethe sets $loc_l^i$ to the column of the first pixel with a human presence and $loc_r^i$ to the column of the last pixel with a human presence. In this way, Lethe identifies the region a person is located in for each frame.

Once $loc_l^i$ and $loc_r^i$ for a human region have been identified the challenge becomes turning this information into a direction using limited memory. While we could retain each region for every frame and process the information once the event is over -- this would mean storing values double the number of frames in an event in memory. Since there is no limit on the number of frames in an event (a person could stand in the doorway for multiple minutes before walking through), this would not allow Lethe to maintain memory limitations. Instead, Lethe accumulates information about crossing direction by comparing only two regions at any given time. Each frame's region is compared to the stored region of the previous frame and assigned a direction indicator value: 1 if the region has shifted to the right, -1 if it has shifted to the left. Lethe retains only the sum of these direction indicators, $d_{sum}$, over multiple frames and assigns a direction, either left or right, based on the negative or positive value of $d_{sum}$ respectively at the end of the event.

To detect and remove non-crossing events, Lethe identifies $d_{sum}=0$ as an event where a person entered and left from the same side of the field of view. However, the basic direction algorithm described above will fail in two scenarios: variable walking speeds and non-crossing events with a person on either side of the door. In the case of variable speed events, a person might walk slowly into the door and then quickly out the same side. Here, $d_{sum}$ might equal $1+1+1+1+1-1-1-1 = 2$ as the first five frame pairs indicated right and only the last three indicated left. Hence, the event would be mislabeled as a rightward crossing through the frame. To prevent this, only direction indicators that are different from the last indicator, $d_{ind}$, are added to $d_{sum}$. In our example, $1+1+1+1+1-1-1-1 = 2$ would become $1-1=0$ and the event would be correctly identified as a non-crossing. This makes the algorithm agnostic to walking speed. Non-crossing events with a person on either side of the doorway are more complex. An example of such an event, where two people walk into the field of view to chat across the doorway, can be seen in the figure above. To identify these non-crossing events, we split the direction detection algorithm into two and determine a direction for each side of the doorway independently. Each side detects human regions and accumulates a direction sum (i.e. $d_{sum1}$ or $d_{sum2}$). If $d_{sum1}$ and $d_{sum2}$ both indicate left or both indicate right, the event is given a direction. If both direction sums are 0 or different directions, then Lethe dismisses the event as a non-crossing event. Hence, Lethe now retains 12 pieces of information for any pair of frames: $loc_{l1}^i$, $loc_{r1}^i$, $loc_{l1}^{i-1}$, $loc_{r1}^{i-1}$, $d_{ind1}$, $d_{sum1}$, $loc_{l2}^i$, $loc_{r2}^i$, $loc_{l2}^{i-1}$, $loc_{r2}^{i-1}$, $d_{ind2}$, $d_{sum2}$. With this information, Lethe determines the direction of crossing events and detects when a person has passed through the field of view but has not crossed the threshold.

# Applications
Lethe is an adaptive system that could be utilized for multipule purposes.

### Occupancy Monitoring
A simple application of the Lethe would be to use it to monitor the occupancy level of any multiroom building. For example, a hospital or clinic could use Lethe to quickly determine which rooms are available for use.

### Smart Buildings
Smart buildings would benefit from a room-level occupancy monitoring system. While existing systems, such as motion detectors, could provide binary information on which rooms have occupants, Lethe provides a quantitative value. This allows buildings to go beyond simply turning lights on and off and would allow for dynamically setting HVAC usage.

# Limitations & Future Works

While the Lethe prototype shows the potential of privacy-preserving image processing, there is still work to be done.

### False Detections
While our experiments found a fairly uniform background temperature that was not disturbed by the floor-to-ceiling window in its field of view, the background may not be as uniform in all environments. Non-human hot objects, such as computers or laptops, may present a challenge in in-situ environments. They could either raise the average background temperature or mistakenly be identified as people. Furthermore, Lethe’s use of thermal cameras limits its use to environments that are cooler than human temperatures.

### Limited Resolution
Due to thermal cameras only recently being made available for public domain use they have a limited resolution. Future work would include testing Lethe with a higher resolution and higher frame rate camera to see if our predictions of increased accuracy hold true. A 3 or greater camera system, as opposed to Lethe’s two, could also provide an increase in the accuracy of the system.

### Multi-person Crossings
All testing was performed with a single person crossing through the sensors' field of view. Multi-user occlusion also presents a limitation for Lethe, where people walking side-by-side or in quick succession are mislabeled as only a single crossing. For Lethe, 0.366 seconds must pass before another person can cross the doorway and be accurately detected. Further sensing from multiple viewpoints may mitigate this problem. For example, a camera placed at the top of the doorway could identify when two people cross side by side. Work in this direction may also lead towards solutions to multi-user phenomena, such as a person sitting in the field of view of the cameras while another person crosses through the doorway. An initial two object expansion to tracking in Lethe, where the recorded values in memory are doubled, could be the first step in that direction.

### Virtual Barriers
In our testing, the sensor was mounted to the side of a door and tested to detect the crossing of a physical barrier such as doorways. However, the system could also be modified to detect a crossing inside of a room by limiting the sensors' field of view and creating a "virtual barrier".

### Multi-sensor System
Just as the two binocular cameras in Lethe can localize a person’s heights, future work may look at localizing a person using a privacy-preserving image process in a space using cameras on two or more walls. Finally, would we be able to detect other human movements, such as coarse or fine-grained gestures, with this approach to provide privacy preservation to existing thermal imaging technologies?

# Publications
Griffiths, Erin, Salah Assana, and Kamin Whitehouse. "Privacy-preserving image processing with binocular thermal cameras." _Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies_ 1.4 (2018): 1-25. [\[PDF\]](https://web.archive.org/web/20190727022605id_/https://dam-prod.media.mit.edu/x/2018/10/17/a133-Griffiths_n3mIM1W.pdf)

# Citing

    @article{griffiths2018privacy,
      title={Privacy-preserving image processing with binocular thermal cameras},
      author={Griffiths, Erin and Assana, Salah and Whitehouse, Kamin},
      journal={Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies},
      volume={1},
      number={4},
      pages={1--25},
      year={2018},
      publisher={ACM New York, NY, USA}
    }
