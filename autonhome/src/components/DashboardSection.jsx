import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';

function DashboardSection({ title, measures }) {
  const [open, setOpen] = useState(false);

  // Group measures by label
  const measuresByLabel = measures.reduce((groups, measure) => {
    const group = (groups[measure.label] || []);
    group.push(measure);
    groups[measure.label] = group;
    return groups;
  }, {});

  const handleClick = () => {
    setOpen(!open);
  };

  // Tooltip to show formatted timestamp
  const CustomTooltip = ({ payload, label }) => {
    if (!payload || !payload.length) return null;
    return (
      <div style={{backgroundColor: '#fff', border: '1px solid #999', margin: 0, padding: 3, borderRadius: 5}}>
        <p>{new Date(label).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
        {payload.map((item) => (
          <p style={{color: item.color}} key={item.name}>{`${item.name}: ${item.value}`}</p>
        ))}
      </div>
    );
  }

  return (
    <Card variant="outlined" sx={{ margin: 2, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', textAlign: 'center' }} onClick={handleClick}>
          {title}
        </Typography>
        {open && (
          <Grid container spacing={2}>
            {Object.entries(measuresByLabel).map(([label, labelMeasures]) => (
              <Grid item xs={4} key={label}>
                {/* Gauge for the latest measure */}

                {/* Line chart for all measures */}
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={labelMeasures} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <XAxis dataKey="timestamp" tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
                    <YAxis domain={['auto', 'auto']} />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#0066cc" activeDot={{ r: 8 }} name={`${label} (${labelMeasures[0].unit})`}/>
                  </LineChart>
                </ResponsiveContainer>
              </Grid>
            ))}
          </Grid>
        )}
      </CardContent>
    </Card>
  );
}

export default DashboardSection;
