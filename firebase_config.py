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