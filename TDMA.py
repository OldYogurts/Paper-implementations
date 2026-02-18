#!/usr/bin/env python3
import numpy as np
#  ----> RANDOM TDMA PROTOCOL ATTEMPT 1 ----

class Tx():
	def __init__(self,L):
		self.tx_uid = "";
		self.Buff_len = L;
		self.buffer = [];
	def Fill_buffer(self,Packets):
		for packet in Packets:
			self.buffer.append(packet);
			if (len(self.buffer) > self.Buff_len):
				raise Exception(f'EXCEPTION:  {self.TX_uid} BUFFER OVERFLOW , packets are more than {self.Buff_len}')   
				break;
		return self.buffer
		
class Rx():
	def __init__(self):
		self.rx_uid = "";
		self.assigned_channel = '';
		self.buffer_recieved=[];
		self.buffer_waiting =[];
	def Receive_buffer(self,Packets : list):
		for packet in Packets:
			if paket.uid == self.Rx_uid:
				self.buffer.append(packet);
			else:
				self.bin.append(packet);
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
	def make_Tx(self,N):
		for i in range(N):
			t = f'tx{i}';
			tx = Tx(10);
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

	def make_omega(self,N):
		for i in range(N):
			ch = f'λ{i}';
			self.omega.append(ch);
		return self.omega;
	
	def make_Alpha(self,N,t):
		self.make_omega(N)
		T = self.make_Tx(t);
		M = len(self.omega)
		for i in range(M):
			self.A[self.omega[i]] = T
		return self.A;
	def make_Beta(self,N,r):
		self.make_omega(N);
		R = self.make_Rx(r);
		M = len(self.omega);
		c = 0;
		for i in range(M):
			R[c].assigned_channel = self.omega[i];
			R[c+1].assigned_channel =self.omega[i];
			c+=2;
		return self.B
	
#print("Tx :",  T);
#print("Rx:",  R);
#print("CHANNELS : ", omega);
#print("\n\n A BIG :\n " , A);
#print("\n\n B set : \n " , B);


def RANDOM_TDMA(w,devices):
	ch , A = Generate_System().make_omega(w),Generate_System().make_Alpha(w,devices);
	assigned = {};
	chosen= [];
	while (len(ch) > 0):
		om = len(ch);
		pk = (np.random.randint(0,om));
		txx = len(A[ch[pk]])
		while(True):
			
			mk = np.random.randint(0,txx);
			ass = A[ch[pk]][mk];
			if ass not in chosen:
				break;
		chosen.append(A[ch[pk]][mk]);
		
		assigned[A[ch[pk]][mk].tx_uid] = ch[pk]
		del ch[pk]
	return assigned

	

	
#_--------------------------------------------------------------------
#	UP TO NOW WE HAVE : 
#		--> 8 nodes with Tx_uid 
#		--> 8 nodes with RX_uid
#		--> a way to assighn channels to Tx_uids
#_--------------------------------------------------------------------a

	
#_--------------------------------------------------------------------
#	WE NEED TO : 
#		A) 
#		- make a packet generator with (destination_id,count_of_same_id) (one of the RX) each has equal prob
#		- run generator that makes a random number (x-5000+x) with x big.
#		- do it 10 times and sum counters for each id and send that to Rx_waiting and save packets in large queue; 
#
#		B)
#		- each t_i all Tx buffers must be full before sending --> send , see empty spots of each , grab from large queue and fill them up.
#		- send packets , if rx receives a packets check if id is correct and remove from the waiting counter
#
#		C) 
#		- count total_packets_send in this t_i  and success_ratio (tot_packets_send/8_buffers)  ,total_waiting(8*L - tot_pack_send) and failure ratio (1-success)
#		- plot (succ- t_i) (failure - t_i).
#		- check if all rx_waiting = 0 to end simulation.
#_--------------------------------------------------------------------
## MAKE A PACKET MA DUDE  MUST HAVE A TX_assigned and an RX sending
## THEN WE NEED TO TAKE THE TX_ASSIGNED,


def Generate_await_buffers_in_rx(seed,min_packets,max_packets):
	





def make_large_Packet_queue():

class Run_simulation()
	def __init__(self,L):
		self.large_queue = make_large_Packet_queue();
		self.Tx_buffer_length = L
	def replenish_tx();
	def send_packets();
	def count_in_tti();
	def plot_results??????




if __name__ == "__main__" :

	w ,devices = 4,8 
	for i in range(10):
		print(i,RANDOM_TDMA(w,devices));
	
