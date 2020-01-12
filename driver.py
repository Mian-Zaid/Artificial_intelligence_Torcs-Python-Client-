'''
Created on Apr 4, 2012

@author: lanquarden
'''

import msgParser
import carState
import carControl

class Driver(object):
    '''
    A driver object for the SCRC
    '''

    def __init__(self, stage):
        '''Constructor'''
        self.WARM_UP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = 3
        self.stage = stage
        
        self.parser = msgParser.MsgParser()
        
        self.state = carState.CarState()
        
        self.control = carControl.CarControl()
        
        self.steer_lock = 0.785398


        # self.steer_lock = 1.5
        self.max_speed = 300
        self.prev_rpm = None
        self.remaining=0
    
    def init(self):
        '''Return init string with rangefinder angles'''
        self.angles = [0 for x in range(19)]
        
        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15
        
        for i in range(5, 9):
            self.angles[i] = -20 + (i-5) * 5
            self.angles[18 - i] = 20 - (i-5) * 5
        
        return self.parser.stringify({'init': self.angles})
    
    def drive(self, msg):
        self.state.setFromMsg(msg)
        
        self.steer()
        
        self.gear()
        
        self.speed()
        
        return self.control.toMsg()
    
    def steer(self):
        angle = self.state.angle
        dist = self.state.trackPos
        steer=self.control.getSteer()
        print "angle : ",angle
        print "dist : ",dist
        print "steer : ",steer

        # steer=angle/0.366519
        # self.control.setSteer(steer)

        # steer=((angle*2.72837152)-dist*0.5)
        # setAccel.control.setSteer(steer)

        steer=(angle*3.72837152 - dist*0.5) #0.5
        steer*=2
        if steer>1:
            steer=1
        elif steer<-1:
            steer=-1    
        self.control.setSteer(steer)

    
    def gear(self):
        rpm = self.state.getRpm()
        gear = self.state.getGear()

        speed = self.state.getSpeedX()

        t=self.state.getTrack()



        totalmaxspeed=self.max_speed
        equalparts=totalmaxspeed/6

        if speed>=0 and speed<equalparts*1.5 and t[9]>0 and self.remaining==0:
            gear=1
        elif speed>=equalparts*1.5 and speed<equalparts*2.5 and t[9]>0:
            gear=2    
        elif speed>=equalparts*2.5 and speed<equalparts*3.5 and t[9]>0:
            gear=3   
        elif speed>=equalparts*3.5 and speed<equalparts*4.25 and t[9]>0:
            gear=4 
        elif speed>=equalparts*4.25 and speed<equalparts*5.25 and t[9]>0:
            gear=5
        elif speed>=equalparts*5.25 and speed<equalparts*6 and t[9]>0:
            gear=6  
        # elif speed>=0 and speed<equalparts*1.5 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1
        # elif speed>=equalparts*1.5 and speed<equalparts*2.5 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1    
        # elif speed>=equalparts*2.5 and speed<equalparts*3.5 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1   
        # elif speed>=equalparts*3.5 and speed<equalparts*4.25 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1
        # elif speed>=equalparts*4.25 and speed<equalparts*5.25 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1
        # elif speed>=equalparts*5.25 and speed<equalparts*6 and t[9]<0:
        #     self.control.setBrake(1)
        #     gear-=1                      
        elif t[9]<0 and gear<=1:
            self.control.setGear(1)
            self.control.setAccel(1)
        elif speed<0 and t[9]>0:
            gear=1
        # elif t[9]>=5 and t[9]<=10:
        #     self.control.setBrake(1)
        #     self.control.setGear(1)
        #     self.control.setBrake(0)




        # if speed>=0 and speed<equalparts:
        #     gear=1
        # elif speed>=equalparts and speed<equalparts*2:
        #     gear=2    
        # elif speed>=equalparts*2 and speed<equalparts*3:
        #     gear=3   
        # elif speed>=equalparts*3 and speed<equalparts*4:
        #     gear=4 
        # elif speed>=equalparts*4 and speed<equalparts*5:
        #     gear=5
        # elif speed>=equalparts*5 and speed<equalparts*6:
        #     gear=6                   

        
        # if self.prev_rpm == None:
        #     up = True
        # else:
        #     if (self.prev_rpm - rpm) < 0:
        #         up = True
        #     else:
        #         up = False
        
        # if up and rpm > 7000:
        #     gear += 1
        
        # if not up and rpm < 3000:
        #     gear -= 1
        
        self.control.setGear(gear)
    
    def speed(self):
        
        

        speed = self.state.getSpeedX()
        accel = self.control.getAccel()
        brake = self.control.getBrake()
        # gear=self.state.getGear()
        t=self.state.getTrack()
        gear=self.control.getGear()

        print "speed : ",speed
        print "track 9 : ",t[9]
        
        x=t[9]
        # print "track 10 : ",t[10]
        # print "track 11 : ",t[11]


        # if x>150 and x<=200:
        #     self.remaining=150
        #     brake=0
        #     accel=1
        # elif x>100 and x<150:
        #     if self.remaining==150:
        #         self.remaining=100
        #         brake=0.2
        #         accel=0.8
        #         gear-=1
        #         # self.control.setBrake(0.2)
        #         # self.control.setAccel(0.8)
        #     else:    
        #         brake=0
        #         accel=1
        # elif x>75 and x<100:
        #     if self.remaining==100:
        #         self.remaining=75
        #         brake=0.4
        #         accel=0.6
        #         gear-=1
        #         # self.control.setBrake(0.4)
        #         # self.control.setAccel(0.6)
        #     else:
        #         brake=0.10
        #         accel=1
        # elif x>50 and x<75:
        #     if self.remaining==75:
        #         self.remaining=50
        #         brake=0.6
        #         accel=0.4
        #         gear-=1
        #         # self.control.setBrake(0.6)
        #         # self.control.setAccel(0.4)
        #     else:
        #         brake=0.20
        #         accel=0.5
        # elif x<50 and x>25:
        #     if self.remaining==50:
        #         self.remaining=25
        #         brake=0.8
        #         accel=0.2
        #         # self.control.setBrake(0.8)
        #         # self.control.setAccel(0.2)
        #     else:
        #         brake=0.25
        #         accel=0.25
        # elif x<=25 and x>10:
        #     if self.remaining==25:
        #         self.remaining=0
        #         brake=1
        #         accel=0.1
        #         gear-=1
        #         # self.control.setBrake(1)
        #         # self.control.setAccel(0.1)
        #     else:
        #         brake=0.6
        #         accel=0.1



        # angle = self.state.getAngle()
        # if angle>0 or angle<0:
        #     self.max_speed=self.max_speed*0.8
        # elif angle==0:
        #     self.max_speed=150  


        if x>100 and speed<self.max_speed:
            # brake=0
            accel=1
        elif x>75 and x<100 and speed<self.max_speed:
            # brake=0.10
            accel=1
        elif x>50 and x<75 and speed<self.max_speed:
            # brake=0.20
            accel=0.5
        elif x<50 and x>25 and speed<self.max_speed:
            # brake=0.25
            accel=0.25
        elif x<=25 and x>10 and speed<self.max_speed:
            # brake=0.6
            accel=0.1



        if x<100 and speed>150:
            brake=0.8
        elif x<75 and speed>100:
            brake=0.6
        elif x<50 and speed>80:
            brake=0.4
        else:
            brake=0                



        # elif x<=10 and x>0 and self.control.getGear()!=-1:
        #     brake=1
        #     accel=0


        # elif x<=0 and self.control.getGear()>=1:
        #     brake=0
        #     self.state.setGear(-1)
        # elif x==-1.0 and self.control.getGear()>=1:
        #     self.state.setGear(-1)
        # elif x==-1 and gear>0:
        #     gear=-1                
    

        

        # if speed < self.max_speed:  #0.1
        #     accel += 0.15
        #     if accel > 1:
        #         accel = 1.0
        # else:
        #     accel -= 0.15
        #     if accel < 0:
        #         accel = 0.0
        
        # self.control.setGear(gear)
        print "accel : ",accel
        # print "brake  : ",brake
        # print "gear : ",gear
        self.control.setAccel(accel)
        self.control.setBrake(brake)
        # self.control.setBrake(brake)
        # self.control.setGear(gear)
        # self.control.setBrake(0)
        
    def onShutDown(self):
        pass
    
    def onRestart(self):
        pass
        