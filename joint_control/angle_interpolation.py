'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello
from scipy import interpolate


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        newkeyframes = ([],[],[])

        #time interval 0.01
        #print keyframes[1][0]       #time
        #print keyframes[2][0]     #value
        for i in range(len(keyframes[0])):
            newkeyframes[0].append(keyframes[0][i])
            #compute spline
            def f(x):
                y_points = []
                x_points = []
                for j in range(len(keyframes[1][i])-1):
                    x_points.append(keyframes[1][i][j])
                #print x_points

                for j in range(len(keyframes[2][i])):
                    y_points.append(keyframes[2][i][j][0])
                print y_points

                tck = interpolate.splrep(x_points, y_points)
                return interpolate.splev(x, tck)

            #add new values
            k = keyframes[1][i][0]
            while k <= len(keyframes[1][i]):
                keyframes[1][i].append(k)
                keyframes[2][i].append(f(k))
                k = k + 0.01




        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
