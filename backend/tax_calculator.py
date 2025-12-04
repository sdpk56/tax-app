from typing import Dict, List, Tuple, Optional

def calculate_tax(income: float, regime: str, deductions: float = 0, rebates: Dict = None) -> Dict:
    """
    Calculates income tax based on the provided income and tax regime (old or new).
    Supports deductions and tax rebates.
    
    Args:
        income: Annual income amount
        regime: Tax regime ('old' or 'new')
        deductions: Standard deductions or section 80C/80D claims
        rebates: Dictionary of applicable rebates
    
    Returns:
        Dictionary with detailed tax breakdown including tax amount, effective rate, etc.
    
    Raises:
        ValueError: If regime is not 'old' or 'new'
    """
    tax_slabs = {
        "old": [
            (0, 250000, 0),
            (250001, 500000, 0.05),
            (500001, 1000000, 0.20),
            (1000001, float('inf'), 0.30)
        ],
        "new": [
            (0, 250000, 0),
            (250001, 500000, 0.05),
            (500001, 750000, 0.10),
            (750001, 1000000, 0.15),
            (1000001, 1250000, 0.20),
            (1250001, 1500000, 0.25),
            (1500001, float('inf'), 0.30)
        ]
    }

    if regime not in tax_slabs:
        raise ValueError("Invalid tax regime specified. Must be 'old' or 'new'.")

    selected_slabs = tax_slabs[regime]
    taxable_income = max(0, income - deductions)
    total_tax = 0.0

    for lower_bound, upper_bound, rate in selected_slabs:
        if taxable_income <= lower_bound:
            break

        taxable_in_slab = min(taxable_income, upper_bound) - max(lower_bound, 0)
        if taxable_in_slab > 0:
            total_tax += taxable_in_slab * rate

    # Apply rebates if available
    if rebates:
        for rebate_type, rebate_amount in rebates.items():
            total_tax = max(0, total_tax - rebate_amount)

    # Add surcharge and cess if income exceeds threshold
    surcharge = 0
    if income > 5000000:
        surcharge = total_tax * 0.25
    elif income > 2000000:
        surcharge = total_tax * 0.15
    elif income > 1000000:
        surcharge = total_tax * 0.10

    health_education_cess = (total_tax + surcharge) * 0.04

    final_tax = total_tax + surcharge + health_education_cess

    return {
        "gross_income": income,
        "deductions": deductions,
        "taxable_income": taxable_income,
        "base_tax": round(total_tax, 2),
        "surcharge": round(surcharge, 2),
        "health_education_cess": round(health_education_cess, 2),
        "total_tax": round(final_tax, 2),
        "effective_tax_rate": round((final_tax / income * 100), 2) if income > 0 else 0,
        "tax_per_month": round(final_tax / 12, 2),
        "take_home_annual": round(income - final_tax, 2),
        "take_home_monthly": round((income - final_tax) / 12, 2)
    }


def compare_tax_regimes(income: float, deductions: float = 0) -> Dict:
    """
    Compare tax liability under old and new regimes.
    
    Args:
        income: Annual income
        deductions: Deductions applicable (for old regime)
    
    Returns:
        Comparison dictionary with both regime calculations
    """
    old_regime = calculate_tax(income, "old", deductions)
    new_regime = calculate_tax(income, "new", 0)  # New regime has standard deduction
    
    return {
        "old_regime": old_regime,
        "new_regime": new_regime,
        "savings": round(old_regime["total_tax"] - new_regime["total_tax"], 2),
        "recommended_regime": "old" if old_regime["total_tax"] < new_regime["total_tax"] else "new"
    }


def calculate_tax_slabs_breakdown(income: float, regime: str) -> List[Dict]:
    """
    Generate detailed breakdown of income across tax slabs.
    
    Args:
        income: Annual income
        regime: Tax regime
    
    Returns:
        List of slab breakdowns with tax calculation
    """
    tax_slabs = {
        "old": [
            {"range": "0 - 2.5L", "from": 0, "to": 250000, "rate": 0},
            {"range": "2.5L - 5L", "from": 250001, "to": 500000, "rate": 0.05},
            {"range": "5L - 10L", "from": 500001, "to": 1000000, "rate": 0.20},
            {"range": "10L+", "from": 1000001, "to": float('inf'), "rate": 0.30}
        ],
        "new": [
            {"range": "0 - 2.5L", "from": 0, "to": 250000, "rate": 0},
            {"range": "2.5L - 5L", "from": 250001, "to": 500000, "rate": 0.05},
            {"range": "5L - 7.5L", "from": 500001, "to": 750000, "rate": 0.10},
            {"range": "7.5L - 10L", "from": 750001, "to": 1000000, "rate": 0.15},
            {"range": "10L - 12.5L", "from": 1000001, "to": 1250000, "rate": 0.20},
            {"range": "12.5L - 15L", "from": 1250001, "to": 1500000, "rate": 0.25},
            {"range": "15L+", "from": 1500001, "to": float('inf'), "rate": 0.30}
        ]
    }

    slabs = tax_slabs.get(regime, [])
    breakdown = []

    for slab in slabs:
        if income <= slab["from"]:
            break
        
        # Calculate income in this slab
        lower = max(slab["from"], 0)
        upper = min(income, slab["to"])
        income_in_slab = max(0, upper - lower)
        tax_in_slab = max(0, income_in_slab * slab["rate"])
        
        breakdown.append({
            "range": slab["range"],
            "income_in_slab": round(income_in_slab, 2),
            "rate": f"{slab['rate']*100:.0f}%",
            "tax": round(tax_in_slab, 2)
        })

    return breakdown

# Example usage (for testing)
# print(f"Old regime tax for 700000: {calculate_tax(700000, 'old')}")
# print(f"New regime tax for 700000: {calculate_tax(700000, 'new')}")
# print(f"Old regime tax for 1200000: {calculate_tax(1200000, 'old')}")
# print(f"New regime tax for 1200000: {calculate_tax(1200000, 'new')}")