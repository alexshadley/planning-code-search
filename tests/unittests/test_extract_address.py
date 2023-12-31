from backend.address_lookup import (extract_addresses,
                                    get_data_for_addresses,
                                    Address)


def test_extract():
    """Recreate test case from Alex Barreira's query"""
    address1 = extract_addresses("Do I need a CUA for formula retail at 522 Octavia Street?")
    address2 = extract_addresses("Do I need a CUA for formula retail at 522 Octavia St.?")
    assert address1
    assert address2
    assert address1 == Address(number=522, street='OCTAVIA')


def test_get_data_for_addresses():
    addy = Address(number=522, street='OCTAVIA')
    data = get_data_for_addresses([addy])
    assert data
    assert '522' in data[0]['address'] and data[0]['zoning_use_district'] == 'NCT-HAYES'
