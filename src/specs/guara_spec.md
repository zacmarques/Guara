# GUARA Specification

## 1. System Overview

The GUARA system is a FastAPI-based application designed for academic data management, synchronization, and automated registration with ORCID API (OAuth 2.0). The system operates in cloud environments and provides users with both authenticated and anonymous access capabilities.

## 2. Core Functionality

### 2.1 User Authentication & Account Management
- Users can create accounts with MySQL backend authentication
- Anonymous access mode available for temporary usage
- Session management with secure cookies (HTTP-Only, Secure, SameSite=Strict)

### 2.2 Academic Data Management
- DOI-based article retrieval and synchronization
- Manual entry creation without DOI requirement
- Automatic history tracking for user actions to assist with pre-filled fields

### 2.3 Data Persistence
- MySQL database backend for all user and academic data
- Cloud-native deployment architecture

## 3. Technical Architecture

### 3.1 Framework & Stack
- Python 3.x with FastAPI framework
- Clean code principles and clean architecture
- SQLAlchemy/SQLModel ORM for database operations
- OAuth 2.0 integration with ORCID API

### 3.2 Security Implementation
- Zero-Trust Architecture compliance
- HTTPS/TLS 1.3 enforcement
- At-Rest Encryption (AES-256 GCM) for sensitive data
- PKCE implementation for secure authentication flows
- Rate limiting and circuit breaker patterns for API consumption

### 3.3 Database Schema Requirements
Based on central_producoes_historicas.xlsx analysis:
- User account management with credentials
- Academic production records (DOI, title, author information)
- Historical action tracking for pre-fill assistance
- Session state management for anonymous users

## 4. UX Design Principles

### 4.1 Visual Design Philosophy
- Clarity: Clear visual hierarchy and information presentation
- Simplicity: Minimal interface with functional elements only
- Contrast Focus: High contrast for readability and visual emphasis
- Expressive Visual Hierarchy: Clear typography and spacing relationships
- Maximized Negative Space: Generous whitespace for visual breathing room
- Proportional Composition: Careful attention to proportions and layouts
- Limited Color Palette: Monochromatic or limited color scheme
- Functional Element Limitation: Elimination of non-functional decorative elements
- Typography Significance: Typographic hierarchy for communication and visual interest
- Decorative Element Elimination: No unnecessary visual embellishments

### 4.2 Interface Components
- Minimalist dashboard with core functionality
- Intuitive form-based data entry
- Clear navigation between authenticated and anonymous modes
- Responsive design for various device sizes
- Accessible UI components following WCAG standards

## 5. Implementation Constraints

### 5.1 Code Generation Rules
- No mocks, pseudocodes, MOPs, or placeholders in critical routes
- All generated code must pass Static Application Security Testing (Bandit, Ruff)
- Fail-secure default behavior for unhandled exceptions
- Strict adherence to Constitution.md guidelines

### 5.2 Data Flow Requirements
- Secure credential handling for both authenticated and anonymous sessions
- Automatic data synchronization with ORCID API
- Local data persistence for offline capabilities
- History tracking for pre-fill assistance in user forms

## 6. Deployment & Operational Requirements

### 6.1 Cloud Deployment
- Containerized application for cloud-native deployment
- Scalable architecture with load balancing considerations
- Monitoring and logging integration
- Automated CI/CD pipeline implementation

### 6.2 Performance Metrics
- High-performance data processing capabilities
- Efficient database queries with proper indexing
- Optimized API response times
- Resource utilization monitoring