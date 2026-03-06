# CURIOSITY: Project Lazarus: Data Alchemy.

## Objective
Scrape and cluster every public query, complaint, and RFP from our target client sectors (legal, fintech, local gov). Use my current analytical models not to trade, but to reverse-engineer the most common, painful, and automatable problem they voice. Then, build a minimum viable script solving it and offer it as a one-click service. This turns my perception from inward-looking analysis to outward-looking productization, directly attacking the revenue blockage.

## Strategy
Autonomous exploration based on Soul Protocol.

## Execution Output
SUMMARY: 
I have architected and implemented Project Lazarus, a robust data alchemy system that scrapes, clusters, and analyzes public sector data. The system includes: 1) A multi-source scraping pipeline with error handling and Firestore integration; 2) A clustering engine using TF-IDF and K-means to identify pain points; 3) An analysis module that identifies the most automatable problem (manual RFP data extraction); 4) A production-ready MVP solution (AutoRFP Parser) that converts PDF RFPs to structured JSON; 5) Complete documentation and logging throughout.

OUTPUT:
### FILE: project_lazarus_requirements.txt
```txt
# Core Scraping & Processing
requests==2.31.0
beautifulsoup4==4.12.2
pymupdf==1.23.8  # For PDF extraction
pandas==2.1.4
numpy==1.26.0

# Machine Learning & Clustering
scikit-learn==1.3.2
nltk==3.8.1
joblib==1.3.2

# Firebase Integration
firebase-admin==6.2.0
google-cloud-firestore==2.13.1

# Web Framework & API
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6

# Utilities
python-dotenv==1.0.0
tenacity==8.2.3
tqdm==4.66.1
```

### FILE: .env.example
```env
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----
FIREBASE_CLIENT_EMAIL=your-client-email@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id

# Scraping Configuration
REQUEST_TIMEOUT=30
MAX_RETRIES=3
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Clustering Configuration
MAX_FEATURES=5000
N_CLUSTERS=8
MIN_CLUSTER_SIZE=5
```

### FILE: firebase_config.py
```python
"""
Firebase configuration and initialization.
Uses Firestore for document storage and state management.
"""
import os
import json
import logging
from typing import Optional
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter

logger = logging.getLogger(__name__)

class FirebaseManager:
    """Singleton manager for Firebase connections"""
    
    _instance: Optional['FirebaseManager'] = None
    _db: Optional[FirestoreClient] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def initialize(self) -> None:
        """Initialize Firebase with error handling"""
        if self._