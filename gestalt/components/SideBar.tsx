import React from 'react';
import {
  PanelGroup,
  Panel,
  PanelResizeHandle,
} from 'react-resizable-panels';

const ResizableSidebar: React.FC = () => {
  return (
    <PanelGroup direction="horizontal">
      <Panel defaultSize={20} minSize={10} maxSize={30}>
        <div style={{ padding: '1rem', backgroundColor: '#f0f0f0' }}>
          Sidebar Content
        </div>
      </Panel>
      <PanelResizeHandle />
      <Panel>
        <div style={{ padding: '1rem' }}>
          Main Content
        </div>
      </Panel>
    </PanelGroup>
  );
};

export default ResizableSidebar;
