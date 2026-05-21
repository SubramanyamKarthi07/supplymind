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
import { USE_MOCK, RESPONSE_PLAN_API } from './api/config'

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

  useEffect(() => {
    fetch('https://numerator-cataract-bloating.ngrok-free.dev/api/analytics/inventory-summary')
      .then(r => r.json())
      .then(data => setSummary(data))
      .catch(() => {
        console.log('Using mock inventory summary')
        setSummary(mockInventorySummary)
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
      value:summary.average_days_of_cover,
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
        Inventory summary from Pavan API with mock fallback
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

              {summary.top_critical_skus?.slice(0,3).map((sku,i) => (

                <tr
                  key={sku.sku}
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
                    {sku.sku}
                  </td>

                  <td style={{padding:'10px'}}>
                    {sku.name}
                  </td>

                  <td style={{
                    padding:'10px',
                    color:'#C53030',
                    fontWeight:'bold'
                  }}>
                    {sku.days_of_cover} days
                  </td>

                  <td style={{padding:'10px'}}>
                    {sku.stock}
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
            {summary.forecast_accuracy?.avg_mape}%
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

const tc = (t) =>
  t.startsWith('↑')
    ? '#1A6B3A'
    : t.startsWith('↓')
    ? '#C53030'
    : '#B7791F'

const Suppliers = () => {
    const [suppliers, setSuppliers] = useState(mockSuppliers)

  useEffect(() => {
    fetch('https://numerator-cataract-bloating.ngrok-free.dev/api/analytics/supplier-risks')
      .then(r => r.json())
      .then(data => setSuppliers(data))
      .catch(() => {
        console.log('Using mock supplier data')
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
          <tr
            key={s.id}
            style={{
              background:i%2===0 ? '#F4F6F9' : 'white'
            }}
          >

            <td style={{padding:'10px'}}>

  <Link
    to={`/suppliers/${s.id}`}
    style={{
      color:'#1B2A4A',
      textDecoration:'none',
      fontWeight:'bold'
    }}
  >
    {s.name}
  </Link>

</td>
            <td style={{padding:'10px'}}>{s.city}</td>
            <td style={{padding:'10px'}}>{s.tier}</td>
            <td style={{padding:'10px'}}>{s.otif}%</td>

            <td style={{
              padding:'10px',
              fontWeight:'bold',
              color:rc(s.risk)
            }}>
              {s.risk}
            </td>

            <td style={{
              padding:'10px',
              fontWeight:'bold',
              color:tc(s.trend)
            }}>
              {s.trend}
            </td>
            <td style={{padding:'10px'}}>

  <Link
  to={`/suppliers/${s.id}`}
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
    fetch('https://numerator-cataract-bloating.ngrok-free.dev/api/analytics/disruption-risks')
      .then(r => r.json())
      .then(data => setDisruptions(data))
      .catch(() => console.log('Using mock data'))
  }, [])
  const generatePlan = async (item) => {

  try {

    setResponsePlan('Loading response plan...')

    // FORCE MOCK MODE
    if (USE_MOCK) {

      const mock = mockPlans[item.sku_name]

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
        'Content-Type':'application/json'
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
${data.summary}

Immediate Actions:
${data.actions?.join('\n')}

Alternate Supplier:
${data.alternateSupplier}

Recommended Reorder Quantity:
${data.reorderQuantity}

Monitoring Checklist:
${data.checklist?.join('\n')}
    `)

  } catch (error) {

    console.log('API failed. Using mock fallback.')

    // MOCK FALLBACK
    const mock = mockPlans[item.sku_name]

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

                  {item.urgency === 'Critical' ? (
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
                  ) : (
                    <span style={{color:'#4A5568'}}>
                      Monitoring
                    </span>
                  )}

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
