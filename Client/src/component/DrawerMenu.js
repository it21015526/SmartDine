import React, { useState } from 'react';
import { Drawer, List, ListItem, ListItemText, IconButton, Box } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router-dom';

function DrawerMenu() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const menuItems = [
    { text: 'Customer Turnaround', path: '/customerTurnaround' },
    { text: 'Customer Interaction', path: '/customerInteraction' },
    { text: 'Table Turnover', path: '/TableTurnover' },
    { text: 'Dynamic Resource Allocation', path: '/dynamicresourceallocation' },
    { text: 'Feedback Form', path: 'https://docs.google.com/forms/d/e/1FAIpQLSc8C60quvUjnNnWuE4IhQzrALDY-wYL1u_n7Ozd4A6liYsm0A/viewform', external: true },
  ];

  const handleItemClick = (item) => {
    if (item.external) {
      window.open(item.path, '_blank');  // Opens the external link in a new tab
    } else {
      navigate(item.path);
    }
  };

  return (
    <div>
      <IconButton onClick={toggleDrawer(true)} color="inherit">
        <MenuIcon />
      </IconButton>
      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        <img src={require('../Assets/newIcn.jpeg')} alt = 'le' style={{width : 100,height : 100,marginLeft :80}}/>
        <Box
          sx={{ width: 250 }}
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          <List>
            {menuItems.map((item, index) => (
              <ListItem button key={index} onClick={() => handleItemClick(item)}>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
          <img src={require('../Assets/le.png')} alt = 'le' width='100%' style={{marginTop : 280}}/>
        </Box>
      </Drawer>
    </div>
  );
}

export default DrawerMenu;
