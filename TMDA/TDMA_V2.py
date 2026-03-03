#!/usr/bin/env python3
import numpy as np
import random
import math
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class Packet:
	packet_id : int = None; 
	packet_tx : str = None;
	packet_rx : str = None;
	delay 	  : int = 0;

@dataclass
class System3 :
	channels   	   : int = 4;
	devices_tx 	   : int = 8;
	devices_rx 	   : int = 8;
	L          	   : int = None;
	min_packets_per_rx : int = None;
	max_packets_per_rx : int = None;
	poisson 	   : float = None;

@dataclass
class Metrics:
	tx_id : str  = None;
	tpi   : int  = 0; 
	qi    : int  = 0; 
	ti    : int  = 0;

def setSystemL(system:object,L:int)            : system.L = L;
def setMIN_PACKETS_PER_RX(system:object,m:int) : system.min_packets_per_rx = m;
def setMAX_PACKETS_PER_RX(system:object,M:int) : system.max_packets_per_rx = M;
def setPoisson(system:object,p:float): system.poisson = p;



class Tx():
	def __init__(self,L):
		self.tx_id : str = None;
		self.buf_len : int = L;
		self.current_buf_state : int = 0
		self.buffer : list = [];
		self.packets_transmitted_per_ti : int = 0;
		self.tx_chosen = 0;
	def fill_buffer(self,packets : list) -> list:
		for p in packets:
			self.buffer.append(p);
			if (len(self.buffer) > self.buf_len):
				raise Exception(f'ERROR : Packet overflow buffer has " {len(self.buffer)} " packets, can hold up to " {self.buf_len} "');
				break;
		return self.buffer
	def send_packet(self,packet :object) -> None:
		self.buffer.remove(packet);
		

class Rx():
	def __init__(self):
		self.rx_id = None;
		self.buffer_received = [];
		self.packets_received = 0;
	def receive_packet(self,packet : object) -> None:
		if packet.packet_rx == self.rx_id :
			self.buffer_received.append(packet);
			self.packets_received +=1;
		else:
			raise Exception(f'ERROR : receiver {self.rx_id} got packet with destination " {packet.packet_rx} " ');
	
class Generate_system():
	def __init__(self):
		self.System_tx = [];
		self.System_rx = [];
		self.System_omega = [];
		self.System_alpha = {};
		self.System_beta = {};
		self.System_metrics = [];
	
	def Make_tx(self,System) -> list[object]:
		for i in range(System.devices_tx):
			tx = Tx(System.L);
			tx.tx_id = f'tx{i}'
			self.System_tx.append(tx)
		return self.System_tx
	def Make_rx(self,System)-> list[object] :
		for i in range(System.devices_rx):
			rx = Rx();
			rx.rx_id =f'rx{i}';
			self.System_rx.append(rx);
		return self.System_rx;

	def Make_omega(self,System)-> list[str]:
		for i in range(System.channels):
			ch = f'λ{i}';
			self.System_omega.append(ch);
		return self.System_omega;
	def Make_alpha(self) -> dict[str,list[object]] :
		T = self.System_tx
		ch = len(self.System_omega);
		for i in range(ch):
			self.System_alpha[self.System_omega[i]] = T;
		return self.System_alpha
	def Make_beta(self) -> dict[str,list[object]] :
		R = self.System_rx;
		ch = len(self.System_omega);
		c = 0;
		for i in range(ch):
			self.System_beta[self.System_omega[i]] =[R[c],R[c+1]];
			c+=2;
		return self.System_beta;
	def Make_metrics(self,System) -> list[object]:
		for t in self.System_tx:
			m = Metrics(tx_id = t.tx_id)
			self.System_metrics.append(m);
		return self.System_metrics
# METHODS

def RANDOM_TDMA(System:object ,tx, omega:list[str],alpha:dict[str,object]) -> dict[object,str]:
	assigned = {};
	chosen= [];	
	for i in range(System.channels):
		while(True):
			t =random.choice(tx);
			if t  not in chosen:
				assigned[t] = omega[i];
				chosen.append(t);
				#print(alpha[omega[i]][txx].tx_id);
				break;
	#print(assigned)
	return assigned

def g(a,b,c,x):
	g = ((a*x)/math.log(1+b/(1+x))) +c
	return g 
	

def weight_calc(tx):
	weights = [0,0,0,0,0,0,0,0];
	i = 0;
	for t in tx:
		test = []
		for p in t.buffer: test.append(p.packet_rx);
		w =  1+ len(set(test)) + t.current_buf_state;
		weights[i] =w 
		i+=1
	return weights
			
def RANDOM_TDMA_weighted(System:object,tx:object , omega:list[str]) -> dict[object,str]:
	assigned = {};
	chosen= [];	
	weights = weight_calc(tx);
	c_w = [];
	for i in range(System.channels):
		while(True):
			t =random.choices(tx,weights);
			t = t[0];
			if t  not in chosen:                       			
				assigned[t] = omega[i];
				t.tx_chosen =0;
				chosen.append(t);                	
				l = tx.index(t);
				c_w.append(weights[l]);
				break;
	#print(assigned)
	return assigned

# THIS IS  ABSOLUTE FRESH SHIT 
#def utility_calc(coallitions):
#	assigned = {}
#	for k,v in coallitions.items():
#		pack_ids = [];
#		Utila,Utilb=0,0;
#		
#		for p in v[0].buffer:
#			pack_ids.append(p.packet_rx);
#		Utila = math.log(len(set(pack_ids))+1,10)
#		for p in v[1].buffer:
#			pack_ids.append(p.packet_rx);
#		Utilb = math.log(len(set(pack_ids))+1,10)
#		if (Utila > Utilb):
#			assigned[v[0]] = k;
#		elif(Utila < Utilb):
#			assigned[v[1]] = k;
#		else:
#			m = np.random.randint(0,1);
#			assigned[v[m]] = k;
#		print(Utila,Utilb);
#		
#	return assigned;
#
#def RANDOM_TDMA_impr(System:object,tx , omega:list[str]) -> dict[object,str]:
#	assigned,collabs,t,chosen,l = {}, {} ,tx ,[] ,0 ;
#	while(True):
#		col = [];
#		for i in range(2):
#			while(True):
#				n = np.random.randint(0,System.devices_tx-1);
#				if n not in chosen:
#					chosen.append(n);
#					col.append(n);
#					break;
#		collabs[omega[l]] = [tx[col[0]],tx[col[1]]];
#		l +=1
#		if len(chosen) >=6:
#			break;
#	col = [];		
#	for i in range(8):
#		if i not in chosen:
#			col.append(i)
#	collabs[omega[l]] = [tx[col[0]],tx[col[1]]];
#
#	assigned = utility_calc(collabs);
#	return assigned
#

def generate_long_queue(system :object, rx :object)->list[object]:

		long_queue = [];
		packet_id_incr = 0;
		for r in rx:
			n = np.random.randint(system.min_packets_per_rx,system.max_packets_per_rx);
			buf = [];
			for i in range(n):
				p = Packet(packet_id = packet_id_incr,packet_rx = r.rx_id);
				buf.append(p);
				packet_id_incr +=1;
			long_queue +=buf
	
			#print(f'{buf}\n\n\n')
		random.shuffle(long_queue);
		#print(long_queue);
		return long_queue
		
	

def GiPi(space:int ,long_queue:list[object],system:object,distribution:str ='poisson'):
	packets = [];
	if distribution != "poisson":
		raise NotImplemented("TODO : other random distributions");
		raise 
	while (True):
		packet_number = np.random.poisson(system.poisson);
		if packet_number <= space: break;
	packets= long_queue[:packet_number];
	del long_queue[:packet_number];
	
	#print(packet_number,len(long_queue),packets)
	return packets;
	

def REfill_tx_buffers(tx:object,queue:list[object],system:object) -> None:
	for t in tx:
		space = t.buf_len - t.current_buf_state
		p = GiPi(space,queue,system)
		t.buffer += p;
		t.current_buf_state = len(t.buffer);
		t.packets_transmitted_per_ti = 0;
		#print(t.current_buf_state);


def STAR(tx:object,avail_rx:dict[str,object],d:dict[object,str]) -> None:
	for k,v in d.items():
		#print(f'\n{k.tx_id} -> {v}: {avail_rx[v][0].rx_id}, {avail_rx[v][1].rx_id}\n');
		tx_has_send = False;
		rxa = avail_rx[v][0]
		rxb = avail_rx[v][1]
		for p in k.buffer:
			if (p.packet_rx ==rxa.rx_id )  and ( not tx_has_send ):
				# send(from_tx,to_rx,packet);
				send(k,rxa,p);     
				tx_has_send = True
			elif (p.packet_rx == rxb.rx_id) and ( not tx_has_send ):
				send(k,rxb,p);
				tx_has_send = True
		
			else:
				p.delay +=1;


def send(from_tx:object,to_rx:object,pack_sending:object) -> None:
	pack_sending.packet_tx = from_tx.tx_id
	to_rx.receive_packet(pack_sending);
	from_tx.send_packet(pack_sending);
	from_tx.packets_transmitted_per_ti +=1;



def Update_metrics(metrics:list[object],tx:object) ->None:
	for t in tx:
		try : 
			M_upd = next((m for m in metrics if t.tx_id == m.tx_id));
		except StopIteration:
			
			print(f"ERROR: Metrics for {t.tx_id} failed to Update");
		M_upd.tpi += (t.packets_transmitted_per_ti);
		M_upd.qi  +=(t.current_buf_state);
		M_upd.ti  +=1;
		#print(M_upd)
		


def Calculate_metrics(metrics:list[object],rx:list[object],steps:int) ->list[int]:
	tp = 0;
	di = []
	qLen = 0;
	delay = 0;
	for m in metrics:
		tp +=m.tpi
		qLen+=m.qi/steps	
		try:
			di.append(m.qi/m.tpi)
		except ZeroDivisionError :
			m.tpi +=0.0000001
			di.append(m.qi/m.tpi)

		assert steps == m.ti
	#tp /=len(metrics);
	tp /=steps
	qLen /=8
	delay = sum(di)/len(di)
	print(f'throughput :{tp}\tdelay: {delay}\tqlen : {qLen}\n ')	
	return [tp,delay,qLen];




def plotter_scatter(metrics,m,use_3d = 1):

    plt.figure(figsize=(10, 6))
    met_w = metrics[:m-1]
    met_s= metrics[m:]
	
    if use_3d:
        # 3D mode: [x, y1, y2] format
        x_coords =  [p[0] for p in met_w]
        y1_coords = [p[1] for p in met_w]
        y2_coords = [p[2] for p in met_w]
        
        plt.scatter(x_coords, y1_coords, s=50, alpha=0.7,color='red', label='Average packet Delay, Weighted', marker='o')
        plt.scatter(x_coords, y2_coords, s=50, alpha=0.7, label='Average Queue Length', marker='s')
        x_coords =  [p[0] for p in met_s]
        y1_coords = [p[1] for p in met_s]
        y2_coords = [p[2] for p in met_s]
        
        plt.scatter(x_coords, y1_coords, s=50, alpha=0.7,color='blue' ,label='Average packet Delay,Standard', marker='o')
        plt.scatter(x_coords, y2_coords, s=50, alpha=0.7, label='Average Queue Length', marker='s')
        
    else:
        # 2D mode: [x, y] format (backward compatible)
        x_coords = [p[0] for p in metrics]
        y_coords = [p[1] for p in metrics]
        
        plt.scatter(x_coords, y_coords, s=50, alpha=0.7, label='Points')
        plt.plot(x_coords, y_coords, 'b-', linewidth=2, label='Connecting Line')
        plt.title('Scatter Plot with Line')
    
    plt.xlabel('Throughput, TP')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.show()

def make_system(system):
	g = Generate_system();
	tx = g.Make_tx(system)
	rx = g.Make_rx(system)	
	omega = g.Make_omega(system)
	alpha = g.Make_alpha()
	beta = g.Make_beta()
	metrics = g.Make_metrics(system);
	l = generate_long_queue(system,rx);

	return tx,rx,omega,alpha,beta,metrics,l




def run_simulation(system,points,steps,min_packets,max_packets,imp):
	setMIN_PACKETS_PER_RX(System3,min_packets/8);
	setMAX_PACKETS_PER_RX(System3,max_packets/8);
	met_list = []
	setSystemL(System3,4);
	for m in range(1,points):
		tx,rx,omega,alpha,beta,metrics,l = make_system(System3)
		setPoisson(System3,(m)*0.05)
		for i in range(steps):
			#print(f'\n\n {i} \n\n');
			d =RANDOM_TDMA_weighted(System3,tx,omega);
			REfill_tx_buffers(tx,l,System3);
			STAR(tx,beta,d);
			Update_metrics(metrics,tx)
		met_list.append(Calculate_metrics(metrics,rx,steps) );
	m = len(met_list);
	for m in range(1,points):
		tx,rx,omega,alpha,beta,metrics,l = make_system(System3)
		setPoisson(System3,(m)*0.05)
		for i in range(steps):
			#print(f'\n\n {i} \n\n');
			d =RANDOM_TDMA(System3,tx,omega,alpha);
			REfill_tx_buffers(tx,l,System3);
			STAR(tx,beta,d);
			Update_metrics(metrics,tx)
		met_list.append(Calculate_metrics(metrics,rx,steps) );

	plotter_scatter(met_list,m);


if __name__ == '__main__':
	run_simulation(System3,20,1000,150000,300000,0);
#
#	setMIN_PACKETS_PER_RX(System3,10);
#	setMAX_PACKETS_PER_RX(System3,100);
#	setSystemL(System3,4);
#
#	tx,rx,omega,alpha,beta,metrics,l = make_system(System3);
#	RANDOM_TDMA_weighted(System3,tx,omega,alpha)
#
