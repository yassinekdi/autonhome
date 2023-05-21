import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Select, MenuItem, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';

const timeFilters = {
  '1h': 3600,
  '5h': 5 * 3600,
  '1j': 24 * 3600,
};

function DashboardSection({ title, measures }) {
  const [open, setOpen] = useState(false);
  const [filteredMeasures, setFilteredMeasures] = useState(measures);
  const [timeFilter, setTimeFilter] = useState(timeFilters['1h']);

  // Filter measures by time
  useEffect(() => {
    const now = new Date();
    const timeAgo = new Date(now.getTime() - timeFilter * 1000);
    const filtered = measures.filter(measure => new Date(measure.timestamp) >= timeAgo);
    setFilteredMeasures(filtered);
  }, [measures, timeFilter]);

  // Group measures by label
  const measuresByLabel = filteredMeasures.reduce((groups, measure) => {
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
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', flex: 1 }}>
            <Typography variant="h5" component="div" sx={{ fontWeight: 'bold' }} onClick={handleClick}>
              {title}
            </Typography>
          </Box>
          {open && (
            <Select value={timeFilter} onChange={(event) => setTimeFilter(event.target.value)} sx={{ minWidth: 50, fontSize: '1rem', padding: '0' }}>
              {Object.entries(timeFilters).map(([label, seconds]) => (
                <MenuItem key={label} value={seconds} sx={{ fontSize: '0.8rem' }}>{label}</MenuItem>
              ))}
            </Select>
          
          )}
        </Box>

        {open && (
          <Grid container spacing={2}>
            {Object.entries(measuresByLabel).map(([label, labelMeasures]) => (
              <Grid item xs={4} key={label}>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={labelMeasures} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <XAxis dataKey="timestamp" tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
                    <YAxis domain={['auto', 'auto']} />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#0066cc" name={`${label} (${labelMeasures[0].unit})`}/>
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