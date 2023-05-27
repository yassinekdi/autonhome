import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Select, MenuItem, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';

const timeFilters = {
  '1h': 3600,
  '5h': 5 * 3600,
  '1j': 24 * 3600,
  'Tout': Infinity,
};

function DashboardSection({ title, measures }) {
  const [open, setOpen] = useState(false);
  const [filteredMeasures, setFilteredMeasures] = useState(measures);
  const [timeFilter, setTimeFilter] = useState(timeFilters['1h']);

  // Filter measures by time
  useEffect(() => {
    const now = new Date();
    let filtered = measures;
    if (timeFilter !== Infinity) {
      const timeAgo = new Date(now.getTime() - timeFilter * 1000);
      filtered = measures.filter(measure => new Date(measure.timestamp) >= timeAgo);
    }
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
    <Card variant="outlined" sx={{ margin: 2, boxShadow: 3 }} >
      <CardContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flex: 1 }} onClick={handleClick}>
            <Typography variant="h5" component="div" sx={{ fontWeight: 'bold' }}>
              {title}
            </Typography>
          </Box>
          {open && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <Select value={timeFilter} onChange={(event) => setTimeFilter(event.target.value)} sx={{ minWidth: 50, fontSize: '1rem', padding: '0' }}>
                {Object.entries(timeFilters).map(([label, seconds]) => (
                  <MenuItem key={label} value={seconds} sx={{ fontSize: '0.8rem' }}>{label}</MenuItem>
                ))}
              </Select>
            </Box>
          )}
        </Box>  

        {open && (
            <Grid container spacing={2}>
              {Object.entries(measuresByLabel).map(([label, labelMeasures]) => (
                <Grid item xs={4} key={label}>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '0.5rem' }}>
                    <Typography variant="subtitle1" sx={{ color: '#0066cc', marginRight: '0.5rem' }}>
                      -o-
                    </Typography>
                    <Typography variant="subtitle1" component="div" sx={{ color: '#0066cc' }}>
                      {`${label} (${labelMeasures[0].unit})`}
                    </Typography>
                  </Box>
                  <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={labelMeasures} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                      <XAxis dataKey="timestamp" tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} />
                      <YAxis domain={['auto', 'auto']} />
                      <CartesianGrid strokeDasharray="3 3" />
                      <Tooltip content={<CustomTooltip />} />
                      <Line type="monotone" dataKey="value" stroke="#0066cc" dot={{ stroke: '#0066cc', strokeWidth: 1 }}/>
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