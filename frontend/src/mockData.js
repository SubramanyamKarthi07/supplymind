export const mockPlans = {

  'Electronics Component 64': {
    summary:
      'Electronics Component 64 supplier delay detected due to logistics disruption.',

    actions: [
      'Contact alternate supplier immediately',
      'Increase safety stock',
      'Prioritize critical orders'
    ],

    alternateSupplier:'ABC Electronics Pvt Ltd',

    reorderQuantity:1152,

    checklist:[
      'Monitor stock daily',
      'Track supplier ETA',
      'Review warehouse inventory'
    ]
  },

  'Packaging Component 12': {
    summary:
      'Packaging Component 12 experiencing moderate raw material shortage.',

    actions:[
      'Shift orders to backup vendor',
      'Reduce low priority shipments',
      'Monitor supplier capacity'
    ],

    alternateSupplier:'Global Packaging Solutions',

    reorderQuantity:650,

    checklist:[
      'Review inventory every 48 hours',
      'Monitor procurement status',
      'Coordinate with operations'
    ]
  },

  'Mechanical Component 31': {
    summary:
      'Mechanical Component 31 facing transportation delays and supply risk.',

    actions:[
      'Use emergency logistics support',
      'Increase reorder frequency',
      'Escalate to supply chain manager'
    ],

    alternateSupplier:'Precision Mechanical Industries',

    reorderQuantity:820,

    checklist:[
      'Track shipment movement',
      'Monitor inventory coverage',
      'Update operations team'
    ]
  }

}

export const supplierDetails = {

  'SUP-0112': {
    supplier_id:'SUP-0112',
    name:'Krishna Electronics',
    city:'Bangalore',
    tier:'Tier 2',
    otif:61,
    lead_time:14,
    fill_rate:72,
    risk_score:88,
    risk_tier:'High',
    top_features:[
      'Late deliveries',
      'Low fill rate',
      'OTIF declining'
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
      'SKU-00064',
      'SKU-00312'
    ]
  },

  'SUP-0156': {
    supplier_id:'SUP-0156',
    name:'Mehta Plastics',
    city:'Surat',
    tier:'Tier 2',
    otif:74,
    lead_time:10,
    fill_rate:81,
    risk_score:70,
    risk_tier:'Medium',
    top_features:[
      'Demand spikes',
      'Packaging delays'
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
      'SKU-00123'
    ]
  },

  'SUP-0069': {
    supplier_id:'SUP-0069',
    name:'Global Auto Components',
    city:'Chennai',
    tier:'Tier 1',
    otif:89,
    lead_time:7,
    fill_rate:93,
    risk_score:42,
    risk_tier:'Low',
    top_features:[
      'Stable deliveries',
      'High fill rate',
      'Strong inventory support'
    ],
    trend:[
  {month:'Jan', otif:82},
  {month:'Feb', otif:84},
  {month:'Mar', otif:85},
  {month:'Apr', otif:87},
  {month:'May', otif:89},
  {month:'Jun', otif:91},
],
    skus:[
      'SKU-00201',
      'SKU-00456'
    ]
  }

}
export const mockSuppliers = [
  {
    id:'SUP-0112',
    name:'Krishna Electronics',
    city:'Bangalore',
    tier:'Tier 2',
    otif:61.0,
    risk:'High',
    trend:'↓ Declining'
  },
  {
    id:'SUP-0156',
    name:'Mehta Plastics',
    city:'Surat',
    tier:'Tier 2',
    otif:74.3,
    risk:'High',
    trend:'↓ Declining'
  },
  {
    id:'SUP-0189',
    name:'Sharma Logistics',
    city:'Ahmedabad',
    tier:'Tier 3',
    otif:69.8,
    risk:'High',
    trend:'↓ Declining'
  },
  {
    id:'SUP-0001',
    name:'Biotique',
    city:'Madurai',
    tier:'Tier 3',
    otif:83.44,
    risk:'Medium',
    trend:'↓ Declining'
  },
  {
    id:'SUP-0069',
    name:'Global Auto Components',
    city:'Chennai',
    tier:'Tier 1',
    otif:89,
    risk:'Low',
    trend:'↑ Improving'
  },
  {
    id:'SUP-0045',
    name:'TechParts Mumbai',
    city:'Mumbai',
    tier:'Tier 1',
    otif:91.2,
    risk:'Low',
    trend:'→ Stable'
  },
  {
    id:'SUP-0078',
    name:'Packaging Co Delhi',
    city:'Delhi',
    tier:'Tier 1',
    otif:88.5,
    risk:'Low',
    trend:'↑ Improving'
  },
]
export const mockInventorySummary = {
  total_skus_tracked: 500,
  critical_skus: 3,
  total_inventory_value: 12500000,
  avg_days_of_cover: 43.6,
  forecast_accuracy: {
    avg_mape: 12.8
  },
  top_3_critical: [
    {
      sku:'SKU-00064',
      name:'Electronics Component 64',
      days_of_cover:1.4,
      stock:45
    },
    {
      sku:'SKU-00312',
      name:'Mechanical Component 31',
      days_of_cover:2.1,
      stock:320
    },
    {
      sku:'SKU-00123',
      name:'Packaging Component 12',
      days_of_cover:2.8,
      stock:180
    }
  ]
}