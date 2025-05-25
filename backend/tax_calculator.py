def calculate_tax(income, regime):
    """
    Calculates income tax based on the provided income and tax regime (old or new).
    This function assumes a progressive tax slab system.
    """
    tax_slabs = {
        "old": [
            (0, 250000, 0),    # Up to 2.5L, 0%
            (250001, 500000, 0.05), # 2.5L to 5L, 5%
            (500001, 1000000, 0.20), # 5L to 10L, 20%
            (1000001, float('inf'), 0.30) # Above 10L, 30%
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
    total_tax = 0.0

    for lower_bound, upper_bound, rate in selected_slabs:
        if income <= lower_bound:
            break # Income is below this slab, no more tax from higher slabs

        # Calculate taxable amount within this slab
        taxable_in_slab = min(income, upper_bound) - lower_bound
        if taxable_in_slab > 0:
            total_tax += taxable_in_slab * rate

    return total_tax

# Example usage (for testing)
# print(f"Old regime tax for 700000: {calculate_tax(700000, 'old')}")
# print(f"New regime tax for 700000: {calculate_tax(700000, 'new')}")
# print(f"Old regime tax for 1200000: {calculate_tax(1200000, 'old')}")
# print(f"New regime tax for 1200000: {calculate_tax(1200000, 'new')}")