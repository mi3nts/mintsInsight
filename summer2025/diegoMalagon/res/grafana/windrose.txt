- marker:
    color: rgb(0,60,0)
  name: 0-2 m/s
  r:
    - ${N_0_2}
    - ${NE_0_2}
    - ${E_0_2}
    - ${SE_0_2}
    - ${S_0_2}
    - ${SW_0_2}
    - ${W_0_2}
    - ${NW_0_2}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(0,80,0)
  name: 2-4 m/s
  r:
    - ${N_2_4}
    - ${NE_2_4}
    - ${E_2_4}
    - ${SE_2_4}
    - ${S_2_4}
    - ${SW_2_4}
    - ${W_2_4}
    - ${NW_2_4}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(10,100,0)
  name: 4-6 m/s
  r:
    - ${N_4_6}
    - ${NE_4_6}
    - ${E_4_6}
    - ${SE_4_6}
    - ${S_4_6}
    - ${SW_4_6}
    - ${W_4_6}
    - ${NW_4_6}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(200,200,0)
  name: 6-8 m/s
  r:
    - ${N_6_8}
    - ${NE_6_8}
    - ${E_6_8}
    - ${SE_6_8}
    - ${S_6_8}
    - ${SW_6_8}
    - ${W_6_8}
    - ${NW_6_8}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(150,150,0)
  name: 8-10 m/s
  r:
    - ${N_8_10}
    - ${NE_8_10}
    - ${E_8_10}
    - ${SE_8_10}
    - ${S_8_10}
    - ${SW_8_10}
    - ${W_8_10}
    - ${NW_8_10}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(200,100,0)
  name: 10-12 m/s
  r:
    - ${N_10_12}
    - ${NE_10_12}
    - ${E_10_12}
    - ${SE_10_12}
    - ${S_10_12}
    - ${SW_10_12}
    - ${W_10_12}
    - ${NW_10_12}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(250,80,0)
  name: 12-14 m/s
  r:
    - ${N_12_14}
    - ${NE_12_14}
    - ${E_12_14}
    - ${SE_12_14}
    - ${S_12_14}
    - ${SW_12_14}
    - ${W_12_14}
    - ${NW_12_14}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar
- marker:
    color: rgb(150,50,0)
  name: 14-16 m/s
  r:
    - ${N_14_16}
    - ${NE_14_16}
    - ${E_14_16}
    - ${SE_14_16}
    - ${S_14_16}
    - ${SW_14_16}
    - ${W_14_16}
    - ${NW_14_16}
  text:
    - North
    - N-E
    - East
    - S-E
    - South
    - S-W
    - West
    - N-W
  type: barpolar

font:
  family: Inter, Helvetica, Arial, sans-serif
  size: 8
xaxis:
  type: date
  autorange: true
  automargin: true
yaxis:
  autorange: true
  automargin: true
title:
  automargin: true
  text: Wind Speed Distribution
margin:
  l: 0
  r: 0
  b: 0
  t: 0
configuration:
  displayModeBar: true
  responsive: true
layout:
  legend:
    font:
      size: 16
  polar:
    angularaxis:
      direction: clockwise
      rotation: 90
    radialaxis:
      ticksuffix: ''
      visible: false
      showticklabels: false
  showlegend: false
  title:
    font:
      size: 16
    text: Wind Speed Distribution
  font:
    family: Inter, Helvetica, Arial, sans-serif
  margin:
    l: 0
    r: 0
    b: 0
    t: 0
legend:
  font:
    size: 16
polar:
  angularaxis:
    direction: clockwise
    rotation: 90
  radialaxis:
    ticksuffix: ''
    visible: false
showlegend: true
