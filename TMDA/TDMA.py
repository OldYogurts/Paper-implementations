#!/usr/bin/env python3
import numpy as np
import random
from dataclasses import dataclass
#  ----> RANDOM TDMA PROTOCOL ATTEMPT 1 ----
@dataclass
class Packet:
	packet_id : int
	rx_id : str
#------
class Tx():
	def __init__(self,L):
		self.tx_uid = "";
		self.Buff_len = L;
		self.buffer = [];
	def Fill_buffer(self,Packets):
		for packet in Packets:
			self.buffer.append(packet);
			if (len(self.buffer) > self.Buff_len):
				raise Exception(f'EXCEPTION:  {self.tx_uid} BUFFER OVERFLOW , packets are more than {self.Buff_len}')   
				break;
		return self.buffer
	def remove(self,packet):
		self.buffer.remove(packet);
		
class Rx():
	def __init__(self):
		self.rx_uid = "";
		self.waiting =0;
		self.buffer_received = []
	def Receive_buffer(self,Packets : list):
		for packet in Packets:
			if packet.rx_id == self.Rx_uid:
				self.waiting -= 1;
			else:
				raise Exception(f' Receiver {rx_uid} got a packet for {packet.uid}');
	def success_ratio(self,Packets):
		return len(Packets)/len(self.buffer);
	def failure_ratio(self,Packets):
		try : return len(Packets)/len(self.bin);
		except : return 0;


# system
class Generate_System():
	def __init__(self):
		self.T = [];
		self.R = [];
		self.omega = [];
		self.A = {};
		self.B = {};
	# TODO:
		# MAKE THIS INTO OBJECTS TX RX 
		# TX HAS A BUFFER L and a UID TX_i
		# RX HAS A BUFFER INF_L  and UID RX_i
	def make_Tx(self,N,L):
		for i in range(N):
			t = f'tx{i}';
			tx = Tx(L);
			tx.tx_uid = t
			self.T.append(tx);
		return self.T;
	
	def make_Rx(self,N):
		for i in range(N):
			r = f'rx{i}';
			rx = Rx();
			rx.rx_uid = r
			self.R.append(rx);
		return self.R;
	# TODO 

	def make_omega(self,w):
		for i in range(w):
			ch = f'λ{i}';
			self.omega.append(ch);
		return self.omega;
	
	def make_Alpha(self):
		T = self.T;
		M = len(self.omega)
		for i in range(M):
			self.A[self.omega[i]] = T
		return self.A;
	def make_Beta(self):
		R = self.R;
		M = len(self.omega);
		c = 0;
		for i in range(M):
			self.B[self.omega[i]] = [R[c],R[c+1]];
			c+=2;
		return self.B
	
#print("Tx :",  T);
#print("Rx:",  R);
#print("CHANNELS : ", omega);
#print("\n\n A BIG :\n " , A);
#print("\n\n B set : \n " , B);

### FUNK
 
##### LONG QUEUE 

# is this retarded???
# i fill the amount expected in each rx depending on the number of packets generated with the rx id as sender
def fill_await(rx , count) ->  None:
	rx.waiting = count

def Generate_buffers_to_send(rx,min_packets,max_packets) -> list:
	n = np.random.randint(min_packets,max_packets);
	buffer = []
	queue = [];
	c = 0;
	for i in range(n):
		p = Packet(packet_id = c,rx_id = rx.rx_uid)
		buffer.append(p);
		c+=1;
	fill_await(rx,c);
	return buffer;

def Generate_long_queue(rx,min_packets,max_packets,devices) -> list:
	Long_queue = []
	for i in range(devices):
		buf = Generate_buffers_to_send(rx[i],min_packets,max_packets)
		Long_queue += buf
	random.shuffle(Long_queue);
	return Long_queue
###############
############### FILL TX BUFFER
def grab_from_queue(lq,L) -> list:
	buf = lq[0:L];
	del lq[0:L];
	return buf




def shift_packets(L,tx) -> int:
	space = 0;
	for i in range(len(tx.buffer)):
		if tx.buffer[i] != None:
			L -=1
	space = L
	return space
			
	
def FILL_TX_BUFFER(Long_queue,tx,devices,L) -> None:
	for i in range(devices):
		spaces = shift_packets(L,tx[i]);
		packets = grab_from_queue(Long_queue,spaces)
		tx[i].Fill_buffer(packets)

###############
############### LE protocolz
def RANDOM_TDMA(w,devices,ch,A) -> dict:
	assigned = {};
	chosen= [];
	for i in range(len(ch)):
		while(True):
			txx = np.random.randint(0,devices)
			if A[ch[i]][txx] not in chosen:
				assigned[A[ch[i]][txx]] = ch[i];
				chosen.append(A[ch[i]][txx]);					
				break
	return assigned

###############
###############  SENDER;

def send(tx , reachable_rx) -> None:
	rx = [rx.rx_uid for rx in reachable_rx]
	for p in tx.buffer:
		if p.rx_id in rx:
			if p.rx_id == reachable_rx[0].rx_uid:
				reachable_rx[0].buffer_received.append(p);
				
			
			else:
				reachable_rx[1].buffer_received.append(p)

			tx.remove(p);
		else :
			continue;
					
###############
###############  LE star??

def Star(w,dev,omega,alpha,beta):
		d = RANDOM_TDMA(w,dev,omega,alpha)
		for k,v in d.items():
			print(k.tx_uid,beta[v][0].rx_uid,beta[v][1].rx_uid);
			send(k,beta[v]);


def run_sim(steps,tx,rx,omega,alpha,beta):
	Long_queue  = Generate_long_queue(rx,15,20,devices);
	for i in range(steps):
			FILL_TX_BUFFER(Long_queue,tx,devices,L);
			Star(w,devices,omega,alpha,beta)	


if __name__ == "__main__" :

	w ,devices ,L = 4,8,10
	g = Generate_System();
	tx = g.make_Tx(devices,L);
	rx = g.make_Rx(devices);
	omega = g.make_omega(w);
	alpha = g.make_Alpha();
	beta = g.make_Beta();

	run_sim(100,tx,rx,omega,alpha,beta);

		#for i in range(len(rx)):
	#	t += rx[i].waiting
	#	print(rx[i].rx_uid," ",rx[i].waiting ,t, len(l_q), end =" ");
	#for i in range(200):
	#	print(l_q[i].packet_id,l_q[i].rx_id);	
