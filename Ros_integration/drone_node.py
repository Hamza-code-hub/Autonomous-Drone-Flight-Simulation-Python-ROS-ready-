import rospy
from geometry_msgs.msg import PoseStamped, Twist

class DroneNode:
    def __init__(self):
        rospy.init_node('simple_drone_node')
        self.pose_sub = rospy.Subscriber('/drone/pose', PoseStamped, self.pose_cb)
        self.cmd_pub = rospy.Publisher('/drone/cmd_vel', Twist, queue_size=10)
        self.current_pose = None
        self.rate = rospy.Rate(10)

    def pose_cb(self, msg):
        self.current_pose = msg.pose

    def send_velocity(self, vx, vy, vz=0.0):
        twist = Twist()
        twist.linear.x = vx
        twist.linear.y = vy
        twist.linear.z = vz
        self.cmd_pub.publish(twist)

    def run(self):
        rospy.loginfo("Drone node started")
        while not rospy.is_shutdown():
            if self.current_pose is not None:
                self.send_velocity(0.0, 0.0, 0.0)  # placeholder
            self.rate.sleep()

if __name__ == "__main__":
    node = DroneNode()
    node.run()
