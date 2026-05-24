
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts'

import { supplierDetails } from '../mocks/mockData'
import { SUPPLIER_RISK_API } from '../api/config'

const SupplierDetail = () => {

  const { supplier_id } = useParams()

  const navigate = useNavigate()

  const supplier = supplierDetails[supplier_id]

  const [riskData, setRiskData] = useState(null)

  useEffect(() => {

    fetch(SUPPLIER_RISK_API, {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'ngrok-skip-browser-warning':'true'
      },
      body:JSON.stringify({
        supplier_id:supplier_id
      })
    })

      .then(r => r.json())

      .then(data => {

        console.log('Dhanush API response:', data)

        setRiskData(data)

      })

      .catch(() => {

        console.log('Risk API unavailable')

      })

  }, [supplier_id])

  if (!supplier) {

    return <h2>Supplier not found</h2>

  }

  return (

    <div style={{
      padding:'40px',
      background:'#F4F6F9',
      minHeight:'100vh'
    }}>

      <button
        onClick={() => navigate('/')}
        style={{
          background:'#1B2A4A',
          color:'white',
          border:'none',
          padding:'10px 16px',
          borderRadius:'6px',
          cursor:'pointer',
          marginBottom:'20px'
        }}
      >
        ← Back to Suppliers
      </button>

      <h2>{supplier.name}</h2>

      {/* Supplier Info */}

      <div style={{
        background:'white',
        padding:'20px',
        marginTop:'20px',
        borderRadius:'8px'
      }}>

        <h3>Supplier Info Card</h3>

        <p>Supplier ID: {supplier.supplier_id}</p>

        <p>City: {supplier.city}</p>

        <p>Tier: {supplier.tier}</p>

        <p>Current OTIF: {supplier.otif}%</p>

        <p>Avg Lead Time: {supplier.lead_time} days</p>

        <p>Fill Rate: {supplier.fill_rate}%</p>

      </div>

      {/* Risk Score */}

      <div style={{
        background:'white',
        padding:'20px',
        marginTop:'20px',
        borderRadius:'8px'
      }}>

        <h3>Risk Score Card</h3>

        <p>
          Risk Score:
          {
            riskData?.risk_score
              ? riskData.risk_score
              : ' Risk score unavailable — backend syncing'
          }
        </p>

        <p>
          Risk Tier:
          {
            riskData?.risk_tier
              ? riskData.risk_tier
              : supplier.risk_tier
          }
        </p>

        <h4>Top Contributing Features</h4>

        <ul>

          {
            riskData?.top_features

              ? riskData.top_features.map(f => (
                  <li key={f}>{f}</li>
                ))

              : supplier.top_features?.map(f => (
                  <li key={f}>{f}</li>
                ))
          }

        </ul>

      </div>

      {/* Performance Trend */}

      <div style={{
        background:'white',
        padding:'20px',
        marginTop:'20px',
        borderRadius:'8px',
        height:'300px'
      }}>

        <h3>Performance Trend</h3>

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={supplier.trend}>

            <XAxis dataKey="month" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="otif"
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

      {/* Supplied SKUs */}

      <div style={{
        background:'white',
        padding:'20px',
        marginTop:'20px',
        borderRadius:'8px'
      }}>

        <h3>Supplied SKUs</h3>

        <ul>

          {supplier.skus?.map(sku => (

            <li key={sku}>{sku}</li>

          ))}

        </ul>

      </div>

    </div>

  )
}

export default SupplierDetail