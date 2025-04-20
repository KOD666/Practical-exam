# CRC 

def xor(check, polynomial):
    result = []
    for i in range(len(polynomial)):
        result.append('0' if check[i] == polynomial[i] else '1')
    return ''.join(result)


def crc(data, polynomial):
    n = len(polynomial) 
    padded_data = data + '0' * (n - 1)  
    check = list(padded_data) 
    for i in range(len(data)):
        if check[i] == '1':  
            check[i:i + n] = xor(check[i:i + n], polynomial)
    return ''.join(check[-(n - 1):])


def receiver(data, polynomial):
    print("Data received:", data)
    crcvalue = crc(data[:-len(polynomial) + 1], polynomial)  
    if '1' in crcvalue:
        print("NO Error detected\n")
    else:
        print("error detected\n")


def main():
    data = input("Enter data :")
    polynomial = input("Enter the polynomial: ")
    crcvalue = crc(data, polynomial)
    final_data = data + crcvalue
    print("CRC value is:", crcvalue)
    print("Final data to be sent:", final_data)
    

    receiver(final_data, polynomial)


if __name__ == "__main__":
    main()


# Parity

data = input("Enter the binary data : ")
parity = str(input("Enter the parity you want (even/odd) : "))

if parity != "even" and parity != "odd":
    print("invalid value for parity. exiting")
    exit()

print("Original data : ", data)
print("Parity : ", parity)

def checkParity(data):

    oneCounter = 0

    for i in data:
        if i == "1" :
            oneCounter += 1
         
    return oneCounter

ones = checkParity(data)
print("No. of 1s in data are : ", ones)

def parityMatcher(data, ones,parity):
    if (ones %2 == 0 and parity == "odd") or (ones %2 != 0 and parity == "even"):
        data = data + "1"
        print("After modification : ", data)

    return data

sRes = parityMatcher(data, ones, parity)


def recieverSide(data, parity):

    rOnes = checkParity(data)
    
    print("Data on Reciever side : ", data)
    print("Parity : ", parity)
    print("No. of parity bits : ", rOnes)

    if (rOnes % 2 == 0 and parity == "even") or (rOnes % 2!=0 and parity == "odd"):
        print("no error found")
    
    if (rOnes % 2 == 0 and parity == "odd") or (rOnes % 2!=0 and parity == "even"):
        print("error found")
    
recieverSide(sRes, parity)


# stop and go 

import asyncio

async def receiver(delay, data):
    await asyncio.sleep(delay)
    print("Receiver: Packet received.")
    print("ACK sent.\n")

async def main():
    packet_data = input("Enter Packet Data (space-separated numbers): ")

    packets = packet_data.split()

    for packet in packets:
        print("\nSending Packet:",packet)
        await receiver(5, packet)
        print("Packet is received, sending next packet...\n")

    print("All packets recived")

asyncio.run(main())

# stop and go ARQ

import asyncio
import random

async def receiver(packet):
    
    await asyncio.sleep(random.uniform(0.5, 3.5))
    rand_val = random.random()
    
    if rand_val < 0.4:
        print(f"Packet {packet['id']} received successfully!")
        return "ACK"
    
    elif rand_val < 0.8:
        print(f"Packet {packet['id']} got delayed. Retransmit requested.")
        return "DELAY"
    
    else:
        print(f"Packet {packet['id']} found with errors. Retransmit requested.")
        return "NACK"

async def send_packet(packet, max_retries=3):
    
    for attempt in range(max_retries + 1):
        print(f"Sending packet {packet['id']}: \"{packet['content']}\"...")
        try:
            status = await asyncio.wait_for(receiver(packet), timeout=2.0)
            if status == "ACK":
                print(f"Packet {packet['id']} acknowledged!\n")
                return True
        except asyncio.TimeoutError:
            print(f"Timeout occurred for packet {packet['id']}!")

        if attempt < max_retries:
            print(f"Retransmitting packet {packet['id']} (Attempt {attempt + 1}/{max_retries})...\n")
            await asyncio.sleep(1)
        else:
            print(f"Max retries reached for packet {packet['id']}. Giving up.\n")
            return False

async def transmit_all(packets):
    
    success_count = 0
    for packet in packets:
        if await send_packet(packet):
            success_count += 1
    print(f"Transmission complete: packets delivered.")

async def main():
    choice = input("Choose packet source (1 = predefined, 2 = custom): ").strip()
    
    if choice == "1":
        # Predeined Dicts For Packets
        packets = [
            {"id": 1, "content": "AAJ HOGI Krantii"},
            {"id": 2, "content": "ALLAH HU AKBAR!!!!"},
            {"id": 3, "content": "KYU KARNA HAAI ATTACK"},
            {"id": 4, "content": "JAO PAV BHAJI KHAO"},
            {"id": 5, "content": "PEAS/PEACE"}
        ]
    else:
        packets = []
        count = int(input("How many packets? "))
        for i in range(1, count + 1):
            content = input(f"Packet {i} content: ")
            packets.append({"id": i, "content": content})
    
    await transmit_all(packets)

if __name__ == "__main__":
    asyncio.run(main())

# Go back n

import asyncio
import random

WINDOW_SIZE = 3
TIMEOUT = 2.0
MAX_RETRIES = 3

total_retransmits = 0

async def receiver(packet_id, content):
    await asyncio.sleep(random.uniform(0.5, 2.0))
    rand = random.random()

    if rand < 0.4:
        print(f"Receiver: Packet {packet_id} received successfully.")
        return "ACK"
    elif rand < 0.6:
        print(f"Receiver: Packet {packet_id} delayed or has errors. Retransmit requested.")
        return "NACK"
    else:
        print(f"Receiver: Packet {packet_id} lost.")
        return None

async def send_window(packets, start_index, retry_counts):
    global total_retransmits

    end_index = min(start_index + WINDOW_SIZE, len(packets))
    window = packets[start_index:end_index]

    print(f"\n>> Sending Window: Packets {start_index + 1} to {end_index}")

    for i, packet in enumerate(window):
        idx = start_index + i
        packet_id = packet["id"]
        content = packet["content"]

        if retry_counts[packet_id] >= MAX_RETRIES:
            print(f"Sender: Packet {packet_id} dropped after {MAX_RETRIES} retries.")
            continue

        print(f"Sender: Sending Packet {packet_id} (Attempt {retry_counts[packet_id] + 1})")

        try:
            response = await asyncio.wait_for(receiver(packet_id, content), timeout=TIMEOUT)

            if response == "ACK":
                print(f"Sender: Packet {packet_id} acknowledged.\n")
                retry_counts[packet_id] = 0

            elif response == "NACK":
                retry_counts[packet_id] += 1
                total_retransmits += 1
                print(f"Sender: NACK for Packet {packet_id}. Will retransmit.\n")
                return idx  # retransmit from this packet

        except asyncio.TimeoutError:
            retry_counts[packet_id] += 1
            total_retransmits += 1
            print(f"Sender: Timeout for Packet {packet_id}. Will retransmit.\n")
            return idx  # retransmit from this packet

    return end_index 

async def go_back_n(packets):
    retry_counts = {pkt["id"]: 0 for pkt in packets}
    index = 0

    while index < len(packets):
        next_index = await send_window(packets, index, retry_counts)

        if next_index > index:
            index = next_index
        else:
            print(f">> Retransmitting from Packet {index + 1}...\n")
            await asyncio.sleep(1)

    dropped = 0
    for count in retry_counts.values():
        if count >= MAX_RETRIES:
            dropped += 1
    
    print(f"Total Retransmissions: {total_retransmits}")
    print(f"Packets Delivered: {len(packets) - dropped}")
    print(f"Packets Dropped: {dropped}")

async def main():

    choice = input("Choose packet input (1 = predefined, 2 = custom): ").strip()

    if choice == "1":
        packets = [
            {"id": 1, "content": "1. OS"},
            {"id": 2, "content": "2. CSA"},
            {"id": 3, "content": "3. DBMS"},
            {"id": 4, "content": "4. Math"},
            {"id": 5, "content": "5. CN"}
        ]
    else:
        packets = []
        
        try:
            count = int(input("How many packets? "))
            for i in range(1, count + 1):
                content = input(f"Enter content for Packet {i}: ")
                packets.append({"id": i, "content": content})
        
        except ValueError:
            print("Invalid input. Using default packet.")
            packets = [{"id": 1, "content": "Default message"}]

    await go_back_n(packets)

if __name__ == "__main__":
    asyncio.run(main())

# selective repeat

import random
import time

# Configuration
TOTAL_FRAMES = 8
WINDOW_SIZE = 4
TIMEOUT = 3  # seconds

sent = [False] * TOTAL_FRAMES
acked = [False] * TOTAL_FRAMES
timeouts = [0] * TOTAL_FRAMES
retries = [0] * TOTAL_FRAMES

sender_base = 0
receiver_base = 0
receiver_buffer = {}

MAX_RETRIES = 5

def receiver(seq_num, corrupted):
    global receiver_base

    if corrupted:
        print(f"Receiver: Frame {seq_num} corrupted NACK")
        return "NACK"

    # If in receiver window
    if receiver_base <= seq_num < receiver_base + WINDOW_SIZE:
        if seq_num not in receiver_buffer:
            print(f"Receiver: Frame {seq_num} received  and buffered.")
            receiver_buffer[seq_num] = f"Data-{seq_num}"
        else:
            print(f"Receiver: Duplicate Frame {seq_num} ignored.")
        return "ACK"
    else:
        print(f"Receiver: Frame {seq_num} outside window. Discarded.")
        return None

def deliver_to_app():
    global receiver_base
    delivered = []

    while receiver_base in receiver_buffer:
        data = receiver_buffer.pop(receiver_base)
        delivered.append(data)
        receiver_base += 1

    return delivered

def simulate_sr():
    global sender_base

    print("\n=== Starting Selective Repeat Simulation ===\n")
    while not all(acked):
        print(f"\nSender Window: {[i for i in range(sender_base, min(sender_base + WINDOW_SIZE, TOTAL_FRAMES))]}")
        print(f"Receiver Expecting From: {receiver_base} to {receiver_base + WINDOW_SIZE - 1}")

        for i in range(sender_base, min(sender_base + WINDOW_SIZE, TOTAL_FRAMES)):
            if acked[i]:
                continue

            should_send = not sent[i] or (time.time() - timeouts[i]) >= TIMEOUT

            if should_send:
                if retries[i] >= MAX_RETRIES:
                    print(f"Sender: Frame {i} dropped after {MAX_RETRIES} retries.")
                    acked[i] = True  # Drop and skip
                    continue

                print(f"\nSender: Sending Frame {i} (Retry #{retries[i]})")
                sent[i] = True
                timeouts[i] = time.time()
                retries[i] += 1

                lost = random.random() < 0.2
                corrupted = random.random() < 0.1

                if lost:
                    print(f"Sender: Frame {i} lost in transit ")
                    continue

                response = receiver(i, corrupted)

                if response == "ACK":
                    acked[i] = True
                    # Move sender base forward if possible
                    while sender_base < TOTAL_FRAMES and acked[sender_base]:
                        sender_base += 1
                elif response == "NACK":
                    sent[i] = False  # Mark for resend

        delivered = deliver_to_app()
        for data in delivered:
            print(f"Receiver:  Delivered to application: {data}")

        time.sleep(1)

    print("\n=== All frames handled. Final delivery ===")
    print(receiver_buffer)
    for i in range(receiver_base, TOTAL_FRAMES):
        if i in receiver_buffer:
            print(f"Receiver:  Delivered (Late): {receiver_buffer[i]}")
    print("\nSimulation Complete.")

simulate_sr()

