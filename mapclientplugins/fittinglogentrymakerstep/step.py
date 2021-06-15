'''
MAP Client Plugin Step
'''
import os
import json
from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fittinglogentrymakerstep.configuredialog import ConfigureDialog


class FittingLogEntryMakerStep(WorkflowStepMountPoint):
    '''
    Step for formatting fitting errors into a log entry string.
    '''

    def __init__(self, location):
        super(FittingLogEntryMakerStep, self).__init__('FittingLogEntryMaker', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Fitting'
        # Add any other initialisation code here:
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'float'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'float'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'float'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'string'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['String'] = ' '

    def _validateInputs(self):
        print('fitting log entry: validating inputs')
        if isinstance(self.subjectName, str):
            print('subject name:' + str(self.subjectName))
        else:
            print('wrong subjectName type:' + str(self.subjectName.__class__))

        if isinstance(self.rbrRmse, float):
            print('reg rmse:' + str(self.rbrRmse))
        else:
            print('wrong rbrRmse type' + str(self.rbrRmse.__class__))

        if isinstance(self.hmfRmse, float):
            print('hmf rmse:' + str(self.hmfRmse))
        else:
            print('wrong hmfRmse type' + str(self.hmfRmse.__class__))

        if isinstance(self.mfRmse, float):
            print('fit rmse:' + str(self.mfRmse))
        else:
            print('wrong mfRmse type' + str(self.mfRmse.__class__))

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        self._validateInputs()
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._config['String'][-1:] != '\n':
            self._config['String'] = self._config['String'] + '\n'

        self.logEntryLine = self._config['String'] % (self.subjectName, self.rbrRmse, self.hmfRmse, self.mfRmse)
        print('log entry:')
        print(self.logEntryLine)
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''

        if index == 0:
            self.subjectName = str(dataIn)  # String of the subjects name
        elif index == 1:
            self.rbrRmse = float(dataIn)  # Float rigid-body registration RMSE
        elif index == 2:
            self.hmfRmse = float(dataIn)  # Float host-mesh fitting Rmse
        else:
            self.mfRmse = float(dataIn)  # Float mesh fitting RMSE

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        return self.logEntryLine  # String

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
