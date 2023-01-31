"""
In order to accomplish the assignment, the robot will look 
for tokens in front of it and grab the nearest one.
Once the robot has grabbed the silver token, it will look for 
a gold token in front of it, move near it, and release the 
silver token once it is close enough.
Silver tokens will be placed next to gold tokens until every 
silver token is next to a different gold token.

"""


#importing some libraries
from __future__ import print_function
import time
import os 
from sr.robot import * 


# define necessary variables
R = Robot()
timee = 0.8
speed = 30 
a_th = 4.0 
d_th = 0.4 
Silver_Token_nums = []               # for storing the tokens are collected
Gold_Token_nums = []				 # for storing the Gold tokens


# Moving the robot
def drive(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

# Adjusting the angle
def turn(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

# Finding ,grabing and delivering Silver Tokens to a Gold one
def Silver_Token(num_Tokens):
	flag = False
	Token_cd = -1
	# Creating a loop with while loop 
	while num_Tokens > 0:
		if not flag:
			# Searching for a silver token
			dist, rot_y, Token_cd = find_Token(MARKER_TOKEN_SILVER, Silver_Token_nums)
			while dist == -1 or Token_cd == -1:
				turn(speed, timee)
				drive(speed, timee)
				dist, rot_y, Token_cd = find_Token(MARKER_TOKEN_SILVER, Silver_Token_nums)
				if Token_cd != -1:
					print('YES , there is a silver token')
				else:
					print('I cannot see any Tokens. \nI am looking for Silver Token')
			
				time.sleep(1)
				
		else:
			dist, rot_y = new_pos(MARKER_TOKEN_SILVER,Token_cd)

		flag = True
		# Grabbing a Silver Token and delivering to a Gold Token
		if dist < d_th:
			if R.grab():

				print('I caught a Silver Token. I should deliver it to a Gold Silver')
				drive(-speed, timee)
				turn(speed, timee)
				reach_gold(Token_cd)
				num_Tokens -= 1
				drive(-speed, timee)
				turn(speed, timee)
				flag = False

			else:
				print('OOOh somthing went WRONG !')
				exit()	
		elif rot_y < -a_th:
			print("I should turn left ")
			turn(-1.5, timee)
		elif rot_y > a_th:
			print("I should turn right")
			turn(1.5, timee)
		else:
			drive(speed, timee)
# Token_tp: type of the token
# Token_lst: list of tokens 

def find_Token(Token_tp, Token_lst):
	dist = 100
	rot_y = 0
	token_code = -1
	# Checking if a Token is seen by the robot
	for token in R.see():
	
		if (token.dist < dist) and (token.info.marker_type is Token_tp) and (token.info.code not in Token_lst):
			dist = token.dist
			token_code = token.info.code
			rot_y = token.rot_y
	if dist >= 100:
		print('I cannot see any Tokens. \nI am looking for Token!')
		return -1, -1, token_code
	else:
		return dist, rot_y, token_code
# Token_tp: type of the goal token 
# Goal_cd: code of the goal token
def new_pos(Token_tp,Goal_cd):
	for token in R.see():
		if (token.info.code == Goal_cd) and (token.info.marker_type is Token_tp):
			return token.dist, token.rot_y
		
	return -1, -1

# token_cd: code of the silver token
def reach_gold(Token_cd):
	Gold_Token = False
	find_gold_flag = False
	Gold_Token_cd = -1
	
	while not Gold_Token:
		if not find_gold_flag:
			dist, rot_y, Gold_Token_cd = find_Token(MARKER_TOKEN_GOLD, Gold_Token_nums)

			while dist == -1 or Gold_Token_cd == -1:
				turn(speed, timee)
				drive(speed, timee)
				dist, rot_y, Gold_Token_cd = find_Token(MARKER_TOKEN_GOLD, Gold_Token_nums)
				if Gold_Token_cd != -1:
					print('There is a Gold Token')
				else:
					print('I cannot see any Gold Tokens. \nI am looking for Gold Token!')
				time.sleep(1)
		else:
			print('I should deliver it to a Gold Silver')
			dist, rot_y = new_pos(MARKER_TOKEN_GOLD,Gold_Token_cd)

		find_gold_flag = True

		# Releasing the silver token if the gold token is close enough 
		if dist < d_th * 1.5:
			Gold_Token = True
			R.release()
			print('I delivered, correctly')
			Silver_Token_nums.append(Token_cd)
			Gold_Token_nums.append(Gold_Token_cd)
			find_gold_flag = False
		# Turning right 
		elif rot_y > a_th:
		    
			print("I should turn right")
			turn(2, timee)

		# Turning left
		elif rot_y < -a_th:
			print("I should turn left")
			turn(-2, timee)
		
		else:
			drive(25, timee)
# At the begining this message is printed
print('Mission has Started, I am loking for a silver Token')
# After collecting all the Silver Tokens, this message is shown
Silver_Token(6)
print(" Mission Completed")
