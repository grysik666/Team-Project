import plotly.graph_objects as go

class Graphs:
    
    def modify_data(self, Centre, Capacity, House, M):
        Centre_Indexes = []
        Temporary_List = [[] for _ in range(len(Centre))]
        NoOfHouses = int(len(House))
        for i in range(len(Centre)):
            for _ in range(int(Capacity[i])):
                Centre_Indexes.append(i)
        for i in range(len(M)):
            Temporary_List[Centre_Indexes[M[i][0]]].append(M[i][1] - NoOfHouses + 1)  
        return Temporary_List
            
    def plot_graph(self, Centre, Capacity, House, M):
        colors = ['aqua', 'green', 'darkblue', 'gold', 'red', 'orange', 'yellow', 'white']
        ListOfHouses = Graphs.modify_data(self, Centre, Capacity, House, M)
        fig = go.Figure(go.Scattermapbox())
        for i in range(len(ListOfHouses)):
            for j in range(len(ListOfHouses[i])):
                fig.add_trace(go.Scattermapbox(
                    mode = "markers+text+lines",
                    lon = [Centre[i][1], House[ListOfHouses[i][j] - 1][1]],
                    lat = [Centre[i][0], House[ListOfHouses[i][j] - 1][0]],
                    line = {'color': colors[i % len(colors)], 'width': 3},
                    text = ["Centre", "House"],textposition = "bottom right",
                    marker = {'size': 12}))

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 19, 'lat': 52},
                'style': "stamen-terrain",
                'zoom': 5.38})

        fig.show()
