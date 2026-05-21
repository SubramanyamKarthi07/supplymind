export const supplierDetails = {

  'SUP-0112': {
    supplier_id:'SUP-0112',
    name:'Krishna Electronics',
    city:'Bangalore',
    tier:'Tier 2',
    otif:61,
    lead_time:14,
    fill_rate:82,
    risk_score:87,
    risk_tier:'High',

    top_features:[
      'Frequent shipment delays',
      'Low OTIF trend',
      'High lead time variability'
    ],

    trend:[
      {month:'Jan', otif:82},
      {month:'Feb', otif:79},
      {month:'Mar', otif:75},
      {month:'Apr', otif:71},
      {month:'May', otif:66},
      {month:'Jun', otif:61},
    ],

    skus:[
      'Electronics Component 64',
      'Sensor Unit 12',
      'PCB Board 45'
    ]
  },

  'SUP-0156': {
    supplier_id:'SUP-0156',
    name:'Mehta Plastics',
    city:'Surat',
    tier:'Tier 2',
    otif:74,
    lead_time:9,
    fill_rate:89,
    risk_score:68,
    risk_tier:'Medium',

    top_features:[
      'Packaging shortages',
      'Moderate OTIF decline'
    ],

    trend:[
      {month:'Jan', otif:88},
      {month:'Feb', otif:86},
      {month:'Mar', otif:83},
      {month:'Apr', otif:80},
      {month:'May', otif:77},
      {month:'Jun', otif:74},
    ],

    skus:[
      'Packaging Component 12',
      'Plastic Cover 77'
    ]
  },

  'SUP-0189': {
    supplier_id:'SUP-0189',
    name:'Sharma Logistics',
    city:'Ahmedabad',
    tier:'Tier 3',
    otif:69,
    lead_time:16,
    fill_rate:78,
    risk_score:91,
    risk_tier:'High',

    top_features:[
      'Transportation delays',
      'Warehouse bottlenecks'
    ],

    trend:[
      {month:'Jan', otif:85},
      {month:'Feb', otif:83},
      {month:'Mar', otif:79},
      {month:'Apr', otif:76},
      {month:'May', otif:72},
      {month:'Jun', otif:69},
    ],

    skus:[
      'Mechanical Component 31',
      'Hydraulic Unit 18'
    ]
  }

}