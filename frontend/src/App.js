import { useState, useEffect } from 'react'
import './App.css'
import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from 'react-router-dom'
import SupplierDetail
from './pages/SupplierDetail'
import {
  mockPlans,
  mockSuppliers,
  mockInventorySummary
} from './mocks/mockData'
import {
  USE_MOCK,
  RESPONSE_PLAN_API,
  FORECAST_API,
  INVENTORY_API,
  FORECAST_ACCURACY_API,
  SUPPLIER_API,
  DISRUPTION_API
} from './api/config'

/* =========================
   INVENTORY DATA
========================= */

const inventoryData = [
  {
    sku:'SKU-00064',
    name:'Electronics Component 64',
    category:'Electronics',
    stock:45,
    doc:1.4,
    status:'Critical'
  },
  {
    sku:'SKU-00123',
    name:'Packaging Component 12',
    category:'Packaging',
    stock:980,
    doc:6.2,
    status:'Warning'
  },
  {
    sku:'SKU-00201',
    name:'Raw Materials Component 20',
    category:'Raw Materials',
    stock:5200,
    doc:18.5,
    status:'Healthy'
  },
  {
    sku:'SKU-00312',
    name:'Mechanical Component 31',
    category:'Mechanical',
    stock:320,
    doc:2.1,
    status:'Critical'
  },
]

const statusColor = (s) =>
  s === 'Critical'
    ? '#C53030'
    : s === 'Warning'
    ? '#B7791F'
    : '#1A6B3A'

/* =========================
   DASHBOARD
========================= */

const Dashboard = () => {

  const [summary, setSummary] = useState(mockInventorySummary)

  const [forecast, setForecast] = useState(
    mockInventorySummary.forecast_accuracy
  )

  const [summaryStatus, setSummaryStatus] = useState('loading')

  useEffect(() => {

    // Inventory Summary API
     
  fetch(INVENTORY_API,
  {
    headers:{
      'ngrok-skip-browser-warning':'true'
    }
  }
)
    .then(r => r.json())
    .then(data => {
      setSummary(data)
      setSummaryStatus('live')
    })
    .catch(error => {
      console.log('Inventory API error:', error)
      setSummary(mockInventorySummary)
      setSummaryStatus('mock')
    })

    // Forecast Accuracy API
 
  fetch(FORECAST_ACCURACY_API,{
    headers:{
      'ngrok-skip-browser-warning':'true'
    }
  }
)
  .then(r => r.json())
  .then(data => setForecast(data))
  .catch(error => {
    console.log('Forecast API error:', error)
    setForecast(mockInventorySummary.forecast_accuracy)
  })
  }, [])
  const kpis = [
    {
      label:'Total SKUs Tracked',
      value:summary.total_skus_tracked,
      color:'#1B2A4A'
    },
    {
      label:'Critical SKUs',
      value:summary.critical_skus,
      color:'#C53030'
    },
    {
      label:'Total Inventory Value',
      value:`₹${summary.total_inventory_value?.toLocaleString()}`,
      color:'#1A6B3A'
    },
    {
      label:'Average Days of Cover',
      value:summary.avg_days_of_cover,
      color:'#B7791F'
    }
  ]

  return (
    <div style={{
      padding:'40px',
      flex:1,
      background:'#F4F6F9',
      minHeight:'100vh'
    }}>

      <h2 style={{color:'#1B2A4A'}}>
        Command Center
      </h2>

     <p style={{
  color:'#4A5568',
  marginBottom:'30px'
}}>
  {summaryStatus === 'live'
  ? 'Live inventory summary from Pavan API'
  : summaryStatus === 'mock'
  ? 'Showing mock inventory data'
  : 'Loading inventory summary...'}
</p>
      {/* KPI Cards */}

      <div style={{
        display:'flex',
        gap:'16px',
        flexWrap:'wrap',
        marginBottom:'30px'
      }}>

        {kpis.map(k => (
          <div
            key={k.label}
            style={{
              background:'white',
              padding:'20px',
              borderRadius:'8px',
              minWidth:'200px',
              flex:'1',
              boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
            }}
          >

            <p style={{
              color:'#4A5568',
              fontSize:'13px'
            }}>
              {k.label}
            </p>

            <h2 style={{
              color:k.color,
              margin:0
            }}>
              {k.value}
            </h2>

          </div>
        ))}

      </div>

      {/* Widgets */}

      <div style={{
        display:'grid',
        gridTemplateColumns:'2fr 1fr',
        gap:'20px'
      }}>

        {/* Top Critical SKUs */}

        <div style={{
          background:'white',
          borderRadius:'8px',
          padding:'20px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>

          <h3 style={{
            color:'#1B2A4A'
          }}>
            Top 3 Critical SKUs
          </h3>

          <p style={{
            color:'#4A5568'
          }}>
            Click SKU to open Disruptions Center
          </p>

          <table style={{
            width:'100%',
            borderCollapse:'collapse',
            marginTop:'16px'
          }}>

            <thead>
              <tr style={{
                background:'#1B2A4A'
              }}>

                {[
                  'SKU',
                  'Name',
                  'Days of Cover',
                  'Stock'
                ].map(h => (
                  <th
                    key={h}
                    style={{
                      padding:'12px',
                      color:'white',
                      textAlign:'left'
                    }}
                  >
                    {h}
                  </th>
                ))}

              </tr>
            </thead>

            <tbody>

              {summary.top_3_critical?.slice(0,3).map((sku,i) => (
                <tr
                  key={sku.sku_name || sku.sku}
                  onClick={() => alert('Please open Disruptions Center from sidebar')}
                  style={{
                    background:i%2===0 ? '#F4F6F9' : 'white',
                    cursor:'pointer'
                  }}
                >

                  <td style={{
                    padding:'10px',
                    fontWeight:'bold',
                    color:'#1B2A4A'
                  }}>
                    {sku.sku_name || sku.sku}
                  </td>

                  <td style={{padding:'10px'}}>
                    {sku.sku_name || sku.name}
                  </td>

                  <td style={{
                    padding:'10px',
                    color:'#C53030',
                    fontWeight:'bold'
                  }}>
                    {sku.days_of_cover} days
                  </td>

                  <td style={{padding:'10px'}}>
                    -
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* Forecast Accuracy */}

        <div style={{
          background:'white',
          borderRadius:'8px',
          padding:'20px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>

          <h3 style={{
            color:'#1B2A4A'
          }}>
            Forecast Accuracy
          </h3>

          <p style={{
            color:'#4A5568'
          }}>
            Average MAPE
          </p>

          <h1 style={{
            color:'#1A6B3A',
            marginTop:'20px'
          }}>
            {forecast?.avg_mape}%
          </h1>

          <p style={{
            color:'#4A5568'
          }}>
            Lower MAPE means better forecast accuracy.
          </p>

        </div>

      </div>

    </div>
  )
}


/* =========================
   INVENTORY PAGE
========================= */

const Inventory = () => (
  <div style={{
    padding:'40px',
    flex:1
  }}>

    <h2 style={{
      color:'#1B2A4A'
    }}>
      Inventory Positions
    </h2>

    <table style={{
      width:'100%',
      borderCollapse:'collapse',
      marginTop:'20px',
      background:'white',
      borderRadius:'8px',
      overflow:'hidden',
      boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
    }}>

      <thead>
        <tr style={{
          background:'#1B2A4A'
        }}>
          {['SKU ID','Product','Category','Stock','Days of Cover','Status'].map(h => (
            <th
              key={h}
              style={{
                padding:'12px',
                color:'white',
                textAlign:'left'
              }}
            >
              {h}
            </th>
          ))}
        </tr>
      </thead>

      <tbody>
        {inventoryData.map((r,i) => (
          <tr
            key={r.sku}
            style={{
              background:i%2===0 ? '#F4F6F9' : 'white'
            }}
          >

            <td style={{padding:'10px'}}>{r.sku}</td>
            <td style={{padding:'10px'}}>{r.name}</td>
            <td style={{padding:'10px'}}>{r.category}</td>
            <td style={{padding:'10px'}}>{r.stock}</td>
            <td style={{padding:'10px'}}>{r.doc} days</td>

            <td style={{
              padding:'10px',
              fontWeight:'bold',
              color:statusColor(r.status)
            }}>
              {r.status}
            </td>

          </tr>
        ))}
      </tbody>

    </table>
  </div>
)

/* =========================
   SUPPLIERS PAGE
========================= */

const rc = (r) =>
  r==='Low'
    ? '#1A6B3A'
    : r==='Medium'
    ? '#B7791F'
    : '#C53030'

const tc = (t = '') =>
  t.startsWith('↑')
    ? '#1A6B3A'
    : t.startsWith('↓')
    ? '#C53030'
    : '#B7791F'

const Suppliers = () => {
    const [suppliers, setSuppliers] = useState(mockSuppliers)

 useEffect(() => {

  fetch(SUPPLIER_API,
    {
      headers:{
        'ngrok-skip-browser-warning':'true'
      }
    }
  )
    .then(r => r.json())
    .then(data => {
      console.log('Pavan supplier API response:', data)
      
 const fixedSuppliers = data.map((s, index) => ({
  id: s.supplier_id || s.id || index,

  name:
    s.supplier_name ||
    s.name ||
    s.supplier_id ||
    '-',

  city:
    s.city ||
    s.supplier_city ||
    '-',

  tier:
    s.city_tier ||
    s.tier ||
    '-',

  otif:
    s.current_otif ||
    s.otif ||
    s.otif_percent ||
    '-',

  risk:
    s.risk_tier ||
    s.risk ||
    s.risk_level ||
    (
      Number(s.current_otif || s.otif || s.otif_percent) < 70
        ? 'High'
        : Number(s.current_otif || s.otif || s.otif_percent) < 85
        ? 'Medium'
        : 'Low'
    ),

  trend:
    s.trend ||
    s.performance_trend ||
    'Stable'
}))

  setSuppliers(fixedSuppliers)
})
    .catch(error => {

      console.log('Supplier API error:', error)

      setSuppliers(mockSuppliers)
    })

}, [])

  return (
  <div style={{
    padding:'40px',
    flex:1
  }}>

    <h2 style={{
      color:'#1B2A4A'
    }}>
      Supplier Scoreboard
    </h2>

    <p style={{
      color:'#4A5568',
      marginBottom:'20px'
    }}>
      Sorted by risk level — High risk first
    </p>

    <table style={{
      width:'100%',
      borderCollapse:'collapse',
      background:'white',
      borderRadius:'8px',
      overflow:'hidden',
      boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
    }}>

      <thead>
        <tr style={{
          background:'#1B2A4A'
        }}>
          {[
  'Supplier',
  'City',
  'Tier',
  'OTIF %',
  'Risk',
  'Trend',
  'Details'
].map(h => (
            <th
              key={h}
              style={{
                padding:'12px',
                color:'white',
                textAlign:'left'
              }}
            >
              {h}
            </th>
          ))}
        </tr>
      </thead>

      <tbody>
        {suppliers.map((s,i) => (
          <tr key={s.id || s.supplier_id || i}
            style={{
              background:i%2===0 ? '#F4F6F9' : 'white'
            }}
          >

            <td style={{padding:'10px'}}>

  <Link
    to={`/suppliers/${s.id || s.supplier_id}`}
    style={{
      color:'#1B2A4A',
      textDecoration:'none',
      fontWeight:'bold'
    }}
  >
    {s.name || s.supplier_name}
  </Link>

</td>
            <td style={{padding:'10px'}}>{s.city || s.supplier_city || '-'}</td>
            <td style={{padding:'10px'}}>{s.tier || s.city_tier || '-'}</td>
            <td style={{padding:'10px'}}>
  {s.otif !== '-' ? `${s.otif}%` : '-'}
</td>

            <td style={{
              padding:'10px',
              fontWeight:'bold',
              color: rc(s.risk || s.risk_level || s.risk_tier)
            }}>
              {s.risk || s.risk_level || s.risk_tier || '-'}
            </td>

            <td style={{
              padding:'10px',
              fontWeight:'bold',
              color:tc(s.trend || 'Stable')
            }}>
              {s.trend || 'Stable'}
            </td>
            <td style={{padding:'10px'}}>

  <Link
  to={`/suppliers/${s.id || s.supplier_id}`}
  style={{
    color:'#1B2A4A',
    fontWeight:'bold',
    textDecoration:'none'
  }}
>
  View Details
</Link>
</td>

          </tr>
        ))}
      </tbody>

    </table>

  </div>
)
}
/* =========================
   FORECAST PAGE
========================= */
const Forecasts = () => {
  const [skuId, setSkuId] = useState('SKU-00064')
  const [forecastDays, setForecastDays] = useState(30)
  const [forecastResult, setForecastResult] = useState(null)
  const [forecastStatus, setForecastStatus] = useState('idle')

  const generateForecast = () => {
    setForecastStatus('loading')

    fetch(FORECAST_API, {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'ngrok-skip-browser-warning':'true'
      },
      body:JSON.stringify({
        sku_id:skuId,
        forecast_days:Number(forecastDays)
      })
    })
      .then(r => r.json())
      .then(data => {
        console.log('Rahul Forecast API:', data)
        setForecastResult(data)
        setForecastStatus('live')
      })
      .catch(error => {
        console.log('Forecast API error:', error)
        setForecastStatus('mock')
        setForecastResult({
          message:'Forecast API unavailable — showing mock fallback',
          sku_id:skuId,
          forecast_days:forecastDays,
          forecast:[
            {day:1, predicted_demand:120},
            {day:2, predicted_demand:135},
            {day:3, predicted_demand:128}
          ]
        })
      })
  }

  const statusText =
    forecastStatus === 'live'
      ? 'Live forecast generated from Rahul API'
      : forecastStatus === 'mock'
      ? 'Mock forecast data shown because backend is unavailable'
      : forecastStatus === 'loading'
      ? 'Generating forecast...'
      : 'Enter SKU details and generate demand forecast'

  const statusColor =
    forecastStatus === 'live'
      ? '#1A6B3A'
      : forecastStatus === 'mock'
      ? '#B7791F'
      : forecastStatus === 'loading'
      ? '#1B2A4A'
      : '#4A5568'

  return (
    <div style={{
      padding:'40px',
      flex:1,
      background:'#F4F6F9',
      minHeight:'100vh'
    }}>

      <div style={{
        display:'flex',
        justifyContent:'space-between',
        alignItems:'center',
        marginBottom:'25px'
      }}>
        <div>
          <h2 style={{
            color:'#1B2A4A',
            marginBottom:'8px'
          }}>
            Forecast Center
          </h2>

          <p style={{
            color:'#4A5568',
            margin:0
          }}>
            AI-powered demand forecasting using Rahul API
          </p>
        </div>

        <div style={{
          background:'white',
          padding:'10px 16px',
          borderRadius:'20px',
          color:statusColor,
          fontWeight:'bold',
          boxShadow:'0 2px 4px rgba(0,0,0,0.08)'
        }}>
          {forecastStatus === 'live'
            ? 'LIVE API'
            : forecastStatus === 'mock'
            ? 'MOCK MODE'
            : forecastStatus === 'loading'
            ? 'LOADING'
            : 'READY'}
        </div>
      </div>

      <div style={{
        display:'grid',
        gridTemplateColumns:'1fr 1fr 1fr',
        gap:'20px',
        marginBottom:'25px'
      }}>

        <div style={{
          background:'white',
          padding:'20px',
          borderRadius:'10px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{color:'#4A5568'}}>Selected SKU</p>
          <h2 style={{color:'#1B2A4A'}}>{skuId}</h2>
        </div>

        <div style={{
          background:'white',
          padding:'20px',
          borderRadius:'10px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{color:'#4A5568'}}>Forecast Horizon</p>
          <h2 style={{color:'#1B2A4A'}}>{forecastDays} Days</h2>
        </div>

        <div style={{
          background:'white',
          padding:'20px',
          borderRadius:'10px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{color:'#4A5568'}}>Forecast Source</p>
          <h2 style={{color:statusColor}}>
            {forecastStatus === 'live' ? 'Rahul API' : forecastStatus === 'mock' ? 'Mock Data' : 'Pending'}
          </h2>
        </div>

      </div>

      <div style={{
        display:'grid',
        gridTemplateColumns:'1fr 2fr',
        gap:'20px'
      }}>

        <div style={{
          background:'white',
          padding:'24px',
          borderRadius:'10px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>

          <h3 style={{
            color:'#1B2A4A',
            marginTop:0
          }}>
            Generate Forecast
          </h3>

          <p style={{
            color:'#4A5568',
            fontSize:'14px'
          }}>
            Enter SKU ID and forecast duration to generate predicted demand.
          </p>

          <label style={{fontWeight:'bold', color:'#1B2A4A'}}>
            SKU ID
          </label>

          <input
            value={skuId}
            onChange={e => setSkuId(e.target.value)}
            style={{
  padding:'14px',
  width:'100%',
  marginTop:'8px',
  marginBottom:'18px',
  border:'2px solid #CBD5E0',
  borderRadius:'10px',
  fontSize:'16px',
  fontWeight:'480',
  color:'#1B2A4A',
  background:'#FFFFFF',
  outline:'none',
  boxShadow:'0 2px 6px rgba(0,0,0,0.08)'
}}
          />

          <label style={{fontWeight:'bold', color:'#1B2A4A'}}>
            Forecast Days
          </label>

          <input
            type="number"
            value={forecastDays}
            onChange={e => setForecastDays(e.target.value)}
            style={{
  padding:'14px',
  width:'100%',
  marginTop:'8px',
  marginBottom:'20px',
  border:'2px solid #CBD5E0',
  borderRadius:'10px',
  fontSize:'16px',
  fontWeight:'480',
  color:'#1B2A4A',
  background:'#FFFFFF',
  outline:'none',
  boxShadow:'0 2px 6px rgba(0,0,0,0.08)'
}}
          />

          <button
            onClick={generateForecast}
            style={{
              background:'#1B2A4A',
              color:'white',
              border:'none',
              padding:'12px 18px',
              borderRadius:'6px',
              cursor:'pointer',
              width:'100%',
              fontWeight:'bold'
            }}
          >
            Generate Forecast
          </button>

        </div>

        <div style={{
          background:'white',
          padding:'24px',
          borderRadius:'10px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>

          <h3 style={{
            color:'#1B2A4A',
            marginTop:0
          }}>
            Forecast Output
          </h3>

          <p style={{
            color:statusColor,
            fontWeight:'bold'
          }}>
            {statusText}
          </p>

          {forecastResult ? (
            <div style={{
  background:'#F8FAFC',
  padding:'20px',
  borderRadius:'12px',
  border:'1px solid #E2E8F0'
}}>

  <div style={{marginBottom:'16px'}}>
    <p style={{color:'#718096', marginBottom:'4px'}}>
      SKU ID
    </p>

    <h3 style={{color:'#1B2A4A', margin:0}}>
      {forecastResult.sku_id}
    </h3>
  </div>

  <div style={{marginBottom:'16px'}}>
    <p style={{color:'#718096', marginBottom:'4px'}}>
      Forecast Days
    </p>

    <h3 style={{color:'#1B2A4A', margin:0}}>
      {forecastResult.forecast_days} Days
    </h3>
  </div>

  <p style={{
    color:'#718096',
    marginBottom:'10px'
  }}>
    Predicted Demand
  </p>

  <table style={{
    width:'100%',
    borderCollapse:'collapse',
    background:'white',
    borderRadius:'8px',
    overflow:'hidden'
  }}>

    <thead>
      <tr style={{
        background:'#1B2A4A',
        color:'white'
      }}>
        <th style={{padding:'12px', textAlign:'center'}}>Day</th>
        <th style={{padding:'12px', textAlign:'center'}}>Predicted Demand</th>
      </tr>
    </thead>

    <tbody>
      {forecastResult.forecast?.map(item => (
        <tr
          key={item.day}
          style={{borderBottom:'1px solid #E2E8F0'}}
        >
          <td style={{
            padding:'12px',
            textAlign:'center'
          }}>
            {item.day}
          </td>

          <td style={{
            padding:'12px',
            textAlign:'center',
            fontWeight:'bold',
            color:'#1B2A4A'
          }}>
            {item.predicted_demand}
          </td>
        </tr>
      ))}
    </tbody>

  </table>

</div>
          ) : (
            <div style={{
              background:'#F4F6F9',
              padding:'40px',
              borderRadius:'8px',
              textAlign:'center',
              color:'#4A5568'
            }}>
              No forecast generated yet
            </div>
          )}

        </div>

      </div>

    </div>
  )
}

/* =========================
   DISRUPTIONS PAGE
========================= */

const Disruptions = () => {

  const [disruptions, setDisruptions] = useState([
    {
      sku_name:'Electronics Component 64',
      category:'Electronics',
      days_of_cover:1.4,
      urgency:'Critical',
      closing_stock_units:45
    },
    {
      sku_name:'Packaging Component 12',
      category:'Packaging',
      days_of_cover:6.2,
      urgency:'Warning',
      closing_stock_units:980
    },
    {
      sku_name:'Mechanical Component 31',
      category:'Mechanical',
      days_of_cover:2.1,
      urgency:'Critical',
      closing_stock_units:320
    },
  ])

  const [responsePlan, setResponsePlan] = useState('')



  useEffect(() => {

  fetch(DISRUPTION_API, {
    headers:{
      'ngrok-skip-browser-warning':'true'
    }
  })
    .then(r => r.json())
    .then(data => setDisruptions(data))
    .catch(error => {
      console.log('Disruption API error:', error)
      console.log('Using mock data')
    })

}, [])
    
  const generatePlan = async (item) => {

  try {

    setResponsePlan('Loading response plan...')

    // FORCE MOCK MODE
    if (USE_MOCK) {
const mock = mockPlans[item.sku_name] || {
  summary:`${item.sku_name} disruption detected. Backend response plan unavailable.`,
  actions:[
    'Review current stock level',
    'Contact supplier immediately',
    'Prepare alternate procurement option'
  ],
  alternateSupplier:'Backup supplier required',
  reorderQuantity:item.closing_stock_units || 500,
  checklist:[
    'Monitor inventory daily',
    'Track supplier update',
    'Escalate if stock risk increases'
  ]
}
      

      setResponsePlan(`
Situation Summary:
${mock.summary}

Immediate Actions:
${mock.actions.join('\n')}

Alternate Supplier:
${mock.alternateSupplier}

Recommended Reorder Quantity:
${mock.reorderQuantity}

Monitoring Checklist:
${mock.checklist.join('\n')}
      `)

      return
    }

    // REAL API CALL
    const response = await fetch(RESPONSE_PLAN_API, {
      method:'POST',
      headers:{
  'Content-Type':'application/json',
  'ngrok-skip-browser-warning':'true'
},
      body:JSON.stringify({
        sku:item.sku_name
      })
    })

    // BACKEND FAILURE
    if (!response.ok) {
      throw new Error('Backend failed')
    }

    const data = await response.json()

setResponsePlan(`
Situation Summary:
${data?.summary || data?.situation_summary || data?.plan_summary || 'No summary returned'}

Immediate Actions:
${Array.isArray(data?.actions) ? data.actions.join('\n') : data?.actions || data?.immediate_actions || 'No actions returned'}
Alternate Supplier:
${data.alternateSupplier || data.alternate_supplier || 'No alternate supplier returned'}

Recommended Reorder Quantity:
${data.reorderQuantity || data.reorder_quantity || 'No reorder quantity returned'}

Monitoring Checklist:
${Array.isArray(data.checklist) ? data.checklist.join('\n') : data.checklist || data.monitoring_checklist || 'No checklist returned'}
`)

  } catch (error) {

    console.log('API failed. Using mock fallback.')

    // MOCK FALLBACK
   const mock = mockPlans[item.sku_name] || {
  summary:`${item.sku_name} disruption detected. Backend response plan unavailable.`,
  actions:[
    'Review current stock level',
    'Contact supplier immediately',
    'Prepare alternate procurement option'
  ],
  alternateSupplier:'Backup supplier required',
  reorderQuantity:item.closing_stock_units || 500,
  checklist:[
    'Monitor inventory daily',
    'Track supplier update',
    'Escalate if stock risk increases'
  ]
}

     setResponsePlan(`
Situation Summary:
${mock.summary}

Immediate Actions:
${mock.actions.join('\n')}

Alternate Supplier:
${mock.alternateSupplier}

Recommended Reorder Quantity:
${mock.reorderQuantity}

Monitoring Checklist:
${mock.checklist.join('\n')}
    `)
  }
}

  

  return (
    <div style={{
      padding:'40px',
      flex:1,
      background:'#F4F6F9',
      minHeight:'100vh'
    }}>

      <h2 style={{
        color:'#1B2A4A',
        marginBottom:'10px'
      }}>
        Disruptions Center
      </h2>

      <p style={{
        color:'#4A5568',
        marginBottom:'30px'
      }}>
        AI-powered disruption monitoring and response planning
      </p>

      <div style={{
        background:'white',
        borderRadius:'8px',
        padding:'20px',
        boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
      }}>

        <h3 style={{
          marginBottom:'20px',
          color:'#1B2A4A'
        }}>
          At-Risk SKUs
        </h3>

        <table style={{
          width:'100%',
          borderCollapse:'collapse'
        }}>

          <thead>
            <tr style={{
              background:'#1B2A4A'
            }}>

              {[
                'SKU Name',
                'Category',
                'Days of Cover',
                'Urgency',
                'Action'
              ].map(h => (
                <th
                  key={h}
                  style={{
                    padding:'12px',
                    color:'white',
                    textAlign:'left'
                  }}
                >
                  {h}
                </th>
              ))}

            </tr>
          </thead>

          <tbody>

            {disruptions.map((item,i) => (

              <tr
                key={i}
                style={{
                  background:i%2===0 ? '#F4F6F9' : 'white',
                  borderBottom:'1px solid #E2E8F0'
                }}
              >

                <td style={{padding:'10px'}}>
                  {item.sku_name}
                </td>

                <td style={{padding:'10px'}}>
                  {item.category}
                </td>

                <td style={{padding:'10px'}}>
                  {item.days_of_cover} days
                </td>

                <td
                  style={{
                    padding:'10px',
                    fontWeight:'bold',
                    color:
                      item.urgency === 'Critical'
                        ? '#C53030'
                        : '#B7791F'
                  }}
                >
                  {item.urgency}
                </td>

                <td style={{padding:'10px'}}>

  <button
    onClick={() => generatePlan(item)}
    style={{
      background:'#1B2A4A',
      color:'white',
      border:'none',
      padding:'8px 14px',
      borderRadius:'6px',
      cursor:'pointer'
    }}
  >
    Generate Response Plan
  </button>

</td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {responsePlan && (

        <div style={{
          marginTop:'30px',
          background:'white',
          borderRadius:'8px',
          padding:'20px',
          boxShadow:'0 2px 4px rgba(0,0,0,0.1)'
        }}>

          <h3 style={{
            color:'#1B2A4A',
            marginBottom:'16px'
          }}>
            AI Response Plan
          </h3>

          <pre style={{
            whiteSpace:'pre-wrap',
            fontFamily:'inherit',
            lineHeight:'1.7',
            color:'#2D3748'
          }}>
            {responsePlan}
          </pre>

        </div>

      )}

    </div>
  )
}

/* =========================
   MAIN APP
========================= */

function App() {

  const [sidebarOpen, setSidebarOpen] = useState(true)

  const [page, setPage] = useState('dashboard')
  

  return (
    <BrowserRouter>
    <div style={{
      display:'flex',
      minHeight:'100vh',
      background:'#F4F7FB'
    }}>

      {/* Sidebar */}

      {sidebarOpen && (
        <div style={{
          width:'250px',
          background:'#1B2A4A',
          color:'white',
          padding:'30px 20px'
        }}>

          <h1>
            SupplyMind
          </h1>

          <div style={{
            display:'flex',
            flexDirection:'column',
            gap:'20px',
            marginTop:'50px'
          }}>

            <div
              onClick={() => setPage('dashboard')}
              style={{
                cursor:'pointer',
                fontWeight:'bold'
              }}
            >
              📊 Dashboard
            </div>

            <div
              onClick={() => setPage('inventory')}
              style={{
                cursor:'pointer',
                fontWeight:'bold'
              }}
            >
              📦 Inventory
            </div>

            <div
              onClick={() => setPage('suppliers')}
              style={{
                cursor:'pointer',
                fontWeight:'bold'
              }}
            >
              🏭 Suppliers
            </div>

            <div
              onClick={() => setPage('disruptions')}
              style={{
                cursor:'pointer',
                fontWeight:'bold'
              }}
            >
              ⚠️ Disruptions
            </div>
            <div
  onClick={() => setPage('forecasts')}
  style={{
    cursor:'pointer',
    fontWeight:'bold'
  }}
>
  📈 Forecasts
</div>

          </div>
        </div>
      )}

      {/* Main Content */}

      <div style={{flex:1}}>

        {/* Top Bar */}

        <div style={{
          padding:'20px 30px'
        }}>

          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{
              fontSize:'24px',
              background:'none',
              border:'none',
              cursor:'pointer',
              color:'#1B2A4A'
            }}
          >
            ☰
          </button>

        </div>

        {/* Pages */}

       <Routes>

  <Route
    path="/"
    element={
      <>
        {page === 'dashboard' && <Dashboard />}
        {page === 'inventory' && <Inventory />}
        {page === 'suppliers' && <Suppliers />}
        {page === 'disruptions' && <Disruptions />}
        {page === 'forecasts' && <Forecasts />}
      </>
    }
  />

  <Route
    path="/suppliers/:supplier_id"
    element={<SupplierDetail />}
  />

</Routes>           

        


      </div>

    </div>
    </BrowserRouter>
  )
}

export default App
