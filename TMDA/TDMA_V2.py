#!/usr/bin/env python3
import numpy as np
import random
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
	def fill_buffer(self,packets : list) -> list:
		for p in packets:
			self.buffer.append(p);
			if (len(self.buffer) > self.buf_len):
				raise Exception(f'ERROR : Packet overflow buffer has " {len(self.buffer)} " packets, can hold up to " {self.buf_len} "');
				break;
		return self.buffer
	def remove_packet(self,packet :object) -> None:
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
	def Make_metrics(self,System) -> object:
		for t in self.System_tx:
			m = Metrics(tx_id = t.tx_id)
			self.System_metrics.append(m);
		return self.System_metrics
# METHODS

def RANDOM_TDMA(System:object , omega:list[str],alpha:dict[str,object]) -> dict[object,str]:
	assigned = {};
	chosen= [];	
	for i in range(System.channels):
		while(True):
			txx = np.random.randint(0,System.devices_tx)
			if alpha[omega[i]][txx] not in chosen:
				assigned[alpha[omega[i]][txx]] = omega[i];
				chosen.append(alpha[omega[i]][txx]);
				#print(alpha[omega[i]][txx].tx_id);
				break;
	#print(assigned)
	return assigned


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
	for i in range(packet_number):
		packets.append(long_queue[i]);
		del long_queue[i];
	#print(packet_number,len(long_queue),packets)
	return packets;

def REfill_tx_buffers(tx:object,queue:list[object],system:object) -> None:
	for t in tx:

		#print(t.current_buf_state);
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
			if (p.packet_rx ==rxa.rx_id )  and (not tx_has_send):
				send(k,rxa,p);     
				tx_has_send = True
			elif (p.packet_rx == rxb.rx_id) and (not tx_has_send):
				send(k,rxb,p);
				tx_has_send = True
		
			else:
				p.delay +=1;


def send(tx:object,rx:object,p:object) -> None:
	p.packet_tx = tx.tx_id
	rx.receive_packet(p);
	tx.remove_packet(p);
	tx.packets_transmitted_per_ti +=1;



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
		di.append(m.qi/m.tpi)
		assert steps == m.ti
	#tp /=len(metrics);
	tp /=steps
	qLen /=8
	delay = sum(di)/len(di)
	print(f'throughput :{tp}\tdelay: {delay}\tqlen : {qLen}\n ')	
	return [tp,delay,qLen];




def plotter_scatter(metrics,use_3d = 1):

    plt.figure(figsize=(10, 6))
    
    if use_3d:
        # 3D mode: [x, y1, y2] format
        x_coords = [p[0] for p in metrics]
        y1_coords = [p[1] for p in metrics]
        y2_coords = [p[2] for p in metrics]
        
        plt.scatter(x_coords, y1_coords, s=50, alpha=0.7, label='Average packet Delay', marker='o')
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
#
#


#    if use_3d == 1:
#
#	x_coords  = [point[0] for point in metrics]
#	y1_coords = [point[1] for point in metrics]
#	y2_coords = [point[2] for point in metrics]
#
#        plt.scatter(x_coords, y1_coords, s=50, alpha=0.7, label='Points Y1', marker='o')
#        plt.scatter(x_coords, y2_coords, s=50, alpha=0.7, label='Points Y2', marker='s')
#        plt.title('3D Parameter Plot (Dual Y Lines)')
#    else :
#	x_coords = [point[0] for point in metrics]
#	y_coords = [point[1] for point in metrics]
#	
#	plt.figure(figsize=(8, 6))
#	plt.scatter(x_coords, y_coords, s=30, alpha=1)
#    plt.xlabel('TP')
#    plt.ylabel('D')
#    plt.grid(True, alpha=0.3)
#    plt.xlim(left=0)
#    plt.ylim(bottom=0),
#    plt.show()
#

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




def run_simulation(system,points,steps,min_packets,max_packets):
	setMIN_PACKETS_PER_RX(System3,min_packets/8);
	setMAX_PACKETS_PER_RX(System3,max_packets/8);
	met_list = []
	setSystemL(System3,4);
	for m in range(1,points):
		tx,rx,omega,alpha,beta,metrics,l = make_system(System3)
		setPoisson(System3,(m)*0.01)
		for i in range(steps):
			#print(f'\n\n {i} \n\n');
			d =RANDOM_TDMA(System3,omega,alpha);
			REfill_tx_buffers(tx,l,System3);
			STAR(tx,beta,d);
			Update_metrics(metrics,tx)
		met_list.append(Calculate_metrics(metrics,rx,steps));
	plotter_scatter(met_list);



if __name__ == '__main__':

	run_simulation(System3,100,1000,15000,30000);
