"""
Enhanced iterative prompts that progressively deepen the analysis
"""

ITERATION_PROMPTS = {
    1: """
    ITERATION 1: Initial Security and Critical Bug Scan
    
    Perform a high-level security and critical bug analysis:
    - SQL injection vulnerabilities
    - XSS and injection attacks
    - Authentication/authorization flaws
    - Critical exceptions and crashes
    - Memory safety issues
    """,
    
    2: """
    ITERATION 2: Performance and Resource Analysis
    
    Focus on performance and resource management:
    - O(n²) or worse algorithms
    - Memory leaks and resource exhaustion
    - Database query optimization
    - Caching inefficiencies
    - Blocking operations
    """,
    
    3: """
    ITERATION 3: Input Validation and Data Flow
    
    Trace data flow and input validation:
    - Unvalidated user inputs
    - Data sanitization gaps
    - Type confusion vulnerabilities
    - Parameter pollution
    - Boundary condition errors
    """,
    
    4: """
    ITERATION 4: Error Handling and Edge Cases
    
    Examine error handling and edge cases:
    - Unhandled exceptions
    - Information leakage in errors
    - Race conditions
    - Null pointer dereferences
    - Resource cleanup failures
    """,
    
    5: """
    ITERATION 5: Architecture and Design Patterns
    
    Review architecture and design:
    - Violation of SOLID principles
    - Circular dependencies
    - Tight coupling issues
    - Missing abstraction layers
    - Inappropriate design patterns
    """,
    
    6: """
    ITERATION 6: Concurrency and Thread Safety
    
    Analyze concurrent code:
    - Race conditions
    - Deadlock potential
    - Thread safety violations
    - Shared state mutations
    - Synchronization issues
    """,
    
    7: """
    ITERATION 7: Configuration and Environment
    
    Check configuration and deployment:
    - Hardcoded secrets
    - Insecure default configurations
    - Environment-dependent bugs
    - Missing configuration validation
    - Production readiness issues
    """,
    
    8: """
    ITERATION 8: Integration and API Security
    
    Review external integrations:
    - API security flaws
    - Third-party library vulnerabilities
    - Service communication security
    - Data serialization issues
    - Protocol implementation bugs
    """,
    
    9: """
    ITERATION 9: Business Logic and Domain Rules
    
    Examine business logic:
    - Business rule violations
    - Workflow bypasses
    - State machine errors
    - Transaction integrity
    - Domain model inconsistencies
    """,
    
    10: """
    ITERATION 10: Comprehensive Review and Risk Assessment
    
    Final comprehensive review:
    - Systematic risk assessment
    - Attack surface analysis
    - Impact and exploitability review
    - Defense-in-depth evaluation
    - Overall security posture
    """
}

def get_iteration_prompt(iteration_number: int, max_iterations: int) -> str:
    """Get focused prompt for specific iteration"""
    
    if iteration_number <= 10:
        return ITERATION_PROMPTS[iteration_number]
    else:
        # For iterations beyond 10, use progressive deep dive
        return f"""
        ITERATION {iteration_number}: Deep Dive Analysis
        
        Continue your thorough analysis focusing on:
        - Subtle vulnerabilities you may have missed
        - Complex interaction bugs between components  
        - Advanced attack vectors and exploitation paths
        - Long-term maintainability issues
        - System-wide impact of identified issues
        
        Look for patterns and connections between previously found issues.
        """
